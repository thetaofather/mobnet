from __future__ import annotations
import os, time, json, logging, hashlib
from dataclasses import dataclass
from typing import Dict, List, Tuple
import requests
import bittensor as bt
from jobs.models import JobOnChain, LocalVerdict
from jobs.manifest import compute_manifest_sha256
from jobs.executor import execute_hit_payouts

logger = logging.getLogger("jobs.watcher")

@dataclass
class WatcherConfig:
    network: str
    netuid: int
    job_board_url: str
    dispute_delay_blocks: int
    consensus_stake_fraction: float
    envelope_room_uid: int

class JobWatcher:
    def __init__(self, cfg: WatcherConfig, wallet: "bt.wallet", subtensor: "bt.subtensor", metagraph: "bt.metagraph", my_uid: int):
        self.cfg = cfg
        self.wallet = wallet
        self.subtensor = subtensor
        self.metagraph = metagraph
        self.my_uid = my_uid

        os.makedirs("state", exist_ok=True)
        self.verdicts_path = os.path.join("state", "verdicts.json")
        self.exec_path = os.path.join("state", "executed.json")
        self._verdicts = self._load_json(self.verdicts_path, {})
        self._executed = self._load_json(self.exec_path, {})

    def _load_json(self, path: str, default):
        try:
            return json.loads(open(path, "r", encoding="utf-8").read())
        except Exception:
            return default

    def _save_json(self, path: str, obj):
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(obj, f, indent=2, sort_keys=True)
        os.replace(tmp, path)

    def fetch_jobs(self) -> List[JobOnChain]:
        r = requests.get(f"{self.cfg.job_board_url}/jobs", timeout=10)
        r.raise_for_status()
        return [JobOnChain(**j) for j in r.json()]

    def _get_validator_stakes(self) -> List[Tuple[int,float]]:
        stakes = []
        if hasattr(self.metagraph, "S"):
            S = self.metagraph.S
            for uid in range(int(self.metagraph.n)):
                stakes.append((uid, float(S[uid])))
        elif hasattr(self.metagraph, "stake"):
            S = self.metagraph.stake
            for uid in range(int(self.metagraph.n)):
                stakes.append((uid, float(S[uid])))
        else:
            for uid in range(int(self.metagraph.n)):
                stakes.append((uid, 1.0))
        return stakes

    def _stake_fraction(self, approving_uids: List[int]) -> float:
        stakes = self._get_validator_stakes()
        total = sum(s for _, s in stakes) + 1e-12
        approving = sum(s for uid, s in stakes if uid in set(approving_uids))
        return approving / total

    def _executor_uid(self, job_id: str) -> int:
        h = hashlib.sha256(job_id.encode("utf-8")).digest()
        n = int(self.metagraph.n) or 1
        return int.from_bytes(h[:4], "little") % n

    def _is_executor_or_failover(self, job_id: str) -> bool:
        n = int(self.metagraph.n) or 1
        primary = self._executor_uid(job_id)
        if self.my_uid == primary:
            return True
        return self.my_uid == ((primary + 1) % n)

    def _get_balance_planck(self, ss58: str) -> int:
        try:
            bal = self.subtensor.get_balance(ss58)
            return int(bal.rao)
        except Exception:
            return 0

    def _verify_job(self, job: JobOnChain, current_block: int) -> LocalVerdict:
        expected = compute_manifest_sha256(job)
        if expected != job.manifest_sha256:
            return LocalVerdict(job_id=job.job_id, validator_hotkey=self.wallet.hotkey.ss58_address,
                                validator_uid=self.my_uid, observed_block=current_block, ok_to_execute=False,
                                reason="manifest mismatch")

        if job.status not in ("armed", "executed"):
            return LocalVerdict(job_id=job.job_id, validator_hotkey=self.wallet.hotkey.ss58_address,
                                validator_uid=self.my_uid, observed_block=current_block, ok_to_execute=False,
                                reason=f"status={job.status}")

        required = sum(int(p.amount_planck) for p in job.participants)
        bal = self._get_balance_planck(job.escrow_address)
        if bal < required:
            return LocalVerdict(job_id=job.job_id, validator_hotkey=self.wallet.hotkey.ss58_address,
                                validator_uid=self.my_uid, observed_block=current_block, ok_to_execute=False,
                                reason=f"escrow underfunded bal={bal} req={required}")

        ex = self._executed.get(job.job_id)
        if ex:
            exec_block = int(ex.get("executed_block", 0))
            if current_block - exec_block < int(job.terms.dispute_delay_blocks):
                return LocalVerdict(job_id=job.job_id, validator_hotkey=self.wallet.hotkey.ss58_address,
                                    validator_uid=self.my_uid, observed_block=current_block, ok_to_execute=False,
                                    reason=f"dispute delay {current_block-exec_block}/{job.terms.dispute_delay_blocks}")

        return LocalVerdict(job_id=job.job_id, validator_hotkey=self.wallet.hotkey.ss58_address,
                            validator_uid=self.my_uid, observed_block=current_block, ok_to_execute=True, reason="ok")

    def _record_verdict(self, v: LocalVerdict):
        jobv = self._verdicts.setdefault(v.job_id, {})
        jobv[v.validator_hotkey] = v.model_dump()
        self._save_json(self.verdicts_path, self._verdicts)

    def _approving_uids(self, job_id: str) -> List[int]:
        jobv = self._verdicts.get(job_id, {})
        return [int(v.get("validator_uid")) for v in jobv.values() if v.get("ok_to_execute")]

    def _mark_executed(self, job_id: str, block: int):
        info = self._executed.setdefault(job_id, {})
        info.setdefault("executed_block", int(block))
        self._save_json(self.exec_path, self._executed)

    def _already_paid(self, job_id: str) -> bool:
        return bool(self._executed.get(job_id, {}).get("paid", False))

    def _mark_paid(self, job_id: str, tx_hash: str):
        info = self._executed.setdefault(job_id, {})
        info["paid"] = True
        info["payout_tx"] = tx_hash
        info["paid_at"] = time.time()
        self._save_json(self.exec_path, self._executed)

    def tick(self, current_block: int):
        try:
            jobs = self.fetch_jobs()
        except Exception as e:
            logger.warning(f"job fetch failed: {e}")
            return

        for job in jobs:
            v = self._verify_job(job, current_block)
            self._record_verdict(v)

            if job.status == "executed":
                self._mark_executed(job.job_id, current_block)

            approving = self._approving_uids(job.job_id)
            frac = self._stake_fraction(approving)

            if not v.ok_to_execute:
                continue
            if frac < self.cfg.consensus_stake_fraction:
                continue
            if not self._is_executor_or_failover(job.job_id):
                continue
            if self._already_paid(job.job_id):
                continue

            # HIT payout behavior (testnet): distribute escrow balance pro-rata by declared deposits.
            escrow_bal = self._get_balance_planck(job.escrow_address)
            total = sum(int(p.amount_planck) for p in job.participants) or 1
            payouts = [(p.ss58, int(escrow_bal * int(p.amount_planck) / total)) for p in job.participants]

            try:
                substrate = getattr(self.subtensor, "substrate", None)
                if substrate is None:
                    logger.error("subtensor.substrate missing; cannot execute payouts")
                    continue
                signer = self.wallet.hotkey  # keypair
                tx_hash = execute_hit_payouts(substrate, signer, job, payouts)
                self._mark_paid(job.job_id, tx_hash)
                logger.info(f"paid job={job.job_id} tx={tx_hash}")
            except Exception as e:
                logger.exception(f"payout failed job={job.job_id}: {e}")
