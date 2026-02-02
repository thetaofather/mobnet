from __future__ import annotations
import logging
from typing import List, Tuple
from substrateinterface import SubstrateInterface, Keypair
from jobs.models import JobOnChain

logger = logging.getLogger("jobs.executor")

def _balances_transfer_call(substrate: SubstrateInterface, dest_ss58: str, amount_planck: int):
    return substrate.compose_call(
        call_module="Balances",
        call_function="transfer",
        call_params={"dest": dest_ss58, "value": int(amount_planck)},
    )

def execute_hit_payouts(substrate: SubstrateInterface, signer: Keypair, job: JobOnChain, payouts: List[Tuple[str,int]]) -> str:
    logger.info(f"Executing HIT payouts job={job.job_id} recipients={len(payouts)}")
    last_hash = ""
    for dest, amount in payouts:
        call = _balances_transfer_call(substrate, dest, amount)
        ext = substrate.create_signed_extrinsic(call=call, keypair=signer)
        receipt = substrate.submit_extrinsic(ext, wait_for_inclusion=True)
        last_hash = receipt.extrinsic_hash
    return last_hash
