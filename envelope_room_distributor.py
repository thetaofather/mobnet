"""Envelope Room distributor (scaffold).

Purpose:
  - Use the Envelope Room wallet to *stake* MOB-α (this subnet's alpha) to miners as "envelopes".
  - This is optional, but matches the Taofather design: emissions accrue to the Envelope Room UID, then are paid out to mobsters.

How payouts are chosen:
  - mode=equal: split the provided `--amount` equally across miners found in metagraph.
  - mode=weights: use a JSON file (state/payout_weights.json) that maps hotkey->weight.

IMPORTANT:
  - This script uses `btcli stake add` under the hood because subnet alpha behaves like stake units.
  - Adjust this once you finalize the exact payout mechanism (staking vs another alpha transfer method).
"""

import os
import json
import shlex
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple

import click
import bittensor as bt
from bittensor_wallet import Wallet

from taofather.config import ENVELOPE_ROOM_NAME

DEFAULT_WEIGHTS_PATH = Path("state/payout_weights.json")

def _run(cmd: List[str], dry_run: bool) -> Tuple[int, str]:
    if dry_run:
        return 0, "[DRY-RUN] " + " ".join(shlex.quote(c) for c in cmd)
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return p.returncode, p.stdout

def load_weight_map(path: Path) -> Dict[str, float]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text())
    return {k: float(v) for k, v in data.items()}

@click.command()
@click.option("--network", default=lambda: os.getenv("NETWORK", "finney"), show_default=True)
@click.option("--netuid", type=int, default=lambda: int(os.getenv("NETUID", "1")), show_default=True)
@click.option("--wallet-name", default=lambda: os.getenv("WALLET_NAME", "default"), show_default=True,
             help="Envelope Room coldkey name (source of rewards).")
@click.option("--wallet-hotkey", default=lambda: os.getenv("HOTKEY_NAME", "default"), show_default=True,
             help="Envelope Room hotkey name (source of rewards).")
@click.option("--mode", type=click.Choice(["equal","weights"], case_sensitive=False), default="equal",
             show_default=True)
@click.option("--amount", type=float, default=1.0, show_default=True,
             help="Total MOB-α amount to distribute this run (interpreted as subnet alpha stake units).")
@click.option("--weights-path", type=click.Path(dir_okay=False, path_type=Path), default=DEFAULT_WEIGHTS_PATH,
             show_default=True)
@click.option("--exclude-hotkey", multiple=True,
             help="Hotkeys (SS58) to exclude from payouts (repeatable).")
@click.option("--dry-run/--live", default=True, show_default=True)
def main(network: str, netuid: int, wallet_name: str, wallet_hotkey: str,
         mode: str, amount: float, weights_path: Path, exclude_hotkey: Tuple[str, ...], dry_run: bool):
    wallet = Wallet(name=wallet_name, hotkey=wallet_hotkey)
    subtensor = bt.Subtensor(network=network)
    metagraph = bt.Metagraph(netuid=netuid, network=network)
    metagraph.sync(subtensor=subtensor)

    excludes = set(exclude_hotkey)
    # Exclude the source hotkey too
    excludes.add(wallet.hotkey.ss58_address)

    # Choose recipients: all hotkeys except excluded
    recipients = [hk for hk in metagraph.hotkeys if hk not in excludes]
    if not recipients:
        raise SystemExit("No eligible recipients (all hotkeys excluded?)")

    if mode.lower() == "equal":
        per = amount / len(recipients)
        payout_pairs = [(hk, per) for hk in recipients]
    else:
        wmap = load_weight_map(weights_path)
        # Only include recipients present in wmap with positive weight
        weighted = [(hk, wmap.get(hk, 0.0)) for hk in recipients]
        weighted = [(hk, w) for hk, w in weighted if w > 0]
        if not weighted:
            raise SystemExit(f"No positive weights found in {weights_path}.")
        total_w = sum(w for _, w in weighted)
        payout_pairs = [(hk, amount * (w/total_w)) for hk, w in weighted]

    click.echo(f"{ENVELOPE_ROOM_NAME}: distributing total={amount:.6f} MOB-α to {len(payout_pairs)} recipients (mode={mode})")
    click.echo(f"Source wallet: {wallet_name} / {wallet_hotkey} ({wallet.hotkey.ss58_address})")
    click.echo(f"Network={network}, netuid={netuid}, dry_run={dry_run}")

    # Execute btcli stake add for each recipient
    # NOTE: btcli uses wallet-name + hotkey-ss58-address (target) + amount
    for hk, amt in payout_pairs:
        if amt <= 0:
            continue
        cmd = [
            "btcli", "stake", "add",
            "--netuid", str(netuid),
            "--wallet-name", wallet_name,
            "--hotkey", wallet_hotkey,
            "--hotkey-ss58-address", hk,
            "--no_prompt",
            "--amount", f"{amt:.12f}",
        ]
        rc, out = _run(cmd, dry_run=dry_run)
        if rc == 0:
            click.echo(f"[OK] paid {amt:.6f} -> {hk}")
        else:
            click.echo(f"[ERR] btcli failed for {hk} (amt={amt:.6f})")
            click.echo(out)

if __name__ == "__main__":
    main()
