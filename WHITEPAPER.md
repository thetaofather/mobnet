# Taofather / MOBnet Subnet (Testnet Scaffold)

This repo is a **testnet-ready scaffold** for the Taofather subnet:

- **Validator redirects 100% of miner emissions** to a designated UID (the **Envelope Room**) via `set_weights()`.
- **Job system** for **Hits** (sell → TAO payouts) and **Rackets** (buy/stake → target-alpha credits + MOB-α envelopes).
- **Validator automatic co-sign** flow with a short **dispute delay** (default **100 blocks**) and a deterministic **failover executor**.

> ⚠️ **Security note**  
> A minimal **private boss-submission job board** is included under `private_backend/` so you can test end-to-end,
> but it is **gitignored** by default. Keep it private or move it to a separate private repo.

---

## Repo Layout

- `validator/`
  - `validator.py` — main validator loop + job watcher tick.
  - `envelope_room_distributor.py` — sets weights to route emissions to the Envelope Room UID.
- `jobs/`
  - `models.py` — job schema.
  - `manifest.py` — manifest hashing.
  - `watcher.py` — job polling, readiness checks, dispute delay, consensus gating, execution.
  - `executor.py` — testnet-safe payout executor.
  - `multisig.py` — multisig address derivation helper (for later hardening).
- `scripts/`
  - `run_validator_testnet.sh` — convenience runner.
- `docker/`
  - `Dockerfile.validator`
  - `docker-compose.testnet.yml`
- `private_backend/` (gitignored)
  - Minimal FastAPI + HTML form to create jobs (local testing).

---

## Configuration (ENV)

- `NETWORK` — `test` or `finney` (default: `test`)
- `NETUID` — your subnet netuid (default: `9999` placeholder)
- `ENVELOPE_ROOM_UID` — UID that receives 100% miner emissions (default: `0` placeholder)
- `WALLET_NAME` / `HOTKEY_NAME` — validator wallet names
- `JOB_BOARD_URL` — URL that serves `GET /jobs` (default: `http://127.0.0.1:8088`)
- `DISPUTE_DELAY_BLOCKS` — default `100`
- `CONSENSUS_STAKE_FRACTION` — stake-weighted threshold (default `0.51`)

---

## Quick Start (Local Testnet)

1) Install deps:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2) Run validator:
```bash
export NETWORK=test
export NETUID=9999               # update after you register your subnet
export ENVELOPE_ROOM_UID=0       # update once you know the Envelope Room UID
export WALLET_NAME=yourcold
export HOTKEY_NAME=yourhot
python -m validator.validator
```

3) Optional: run the private job board (local testing only):
```bash
cd private_backend
pip install -r requirements.txt
python -m private_backend.app
```

---

## What is “Envelope Room”?

**Envelope Room** is the destination UID where validators route miner emissions by setting weights 100% to that UID.
This creates a subnet-controlled MOB-α pool used to pay envelopes.

---

## Implemented vs stubbed

✅ Implemented:
- Weight routing to Envelope Room UID (100%).
- Job polling, manifest hashing, dispute delay, deterministic failover executor.
- HIT payouts as **TAO transfers** (Balances pallet) using the validator hotkey (testnet-only).

🧩 Stubbed (wire after launch):
- RACKET staking call (depends on your runtime/pallet call signature).
- True escrow multisig spending (helper provided; execution flow to be added).

---

## DO NOT COMMIT
- `private_backend/` is in `.gitignore` — keep it private.


---

## Custodial Risk & Trust Minimization

A core design goal of **The Taofather** is to minimize custodial risk while still enabling coordinated, high-impact actions.

Unlike centralized systems where a single operator directly controls pooled funds, The Taofather separates **authorization** from **execution**:

- **Participants always fund a job knowingly and explicitly.**  
  Every Hit or Racket uses a **job-specific wallet** created for that job alone. Funds are never mixed across jobs.

- **Validators never custody participant funds.**  
  Validators do not hold, move, or receive pooled assets. Their role is strictly to **verify outcomes and authorize settlement**.

- **Authorization is stake-weighted and public.**  
  Validators independently verify job conditions (fills, thresholds, execution results, and payouts) and publish cryptographic signatures on-chain.  
  A settlement becomes valid only when a **majority of validator stake (≥51%)** agrees on the same payout hash.

- **No single signer can redirect funds.**  
  The canonical payout plan is determined by economic consensus:  
  **the payout hash supported by the highest total validator stake wins** after a short dispute window.

- **Execution is constrained and auditable.**  
  The job wallet executes transfers *only* according to an authorized payout plan.  
  Every input, signature, and outcome is permanently auditable on-chain.

This design ensures that:
- Participants cannot renegotiate or withdraw after committing.
- Validators cannot steal or redirect funds.
- The system does not rely on trust in a single operator.
- Any observer can independently verify that funds moved exactly as authorized.

In short, The Taofather replaces custodial trust with **economic consensus, transparency, and auditability**, aligning incentives across all participants while reducing the risk surface inherent in centralized coordination.
