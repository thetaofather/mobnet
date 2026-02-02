"""Taofather subnet validator (scaffold).

Core behavior:
  - Redirect **100%** of miner incentives to the Taofather-owned UID: **The Envelope Room**.
  - Implemented by setting all weights to the Envelope Room neuron on each tempo.
"""

import os
import sys
import time
import logging
import threading
import click
import bittensor as bt
from bittensor_wallet import Wallet

from taofather.config import ENVELOPE_ROOM_NAME, ENVELOPE_HOTKEY_SS58, ENVELOPE_UID
from taofather.utils import find_uid_by_hotkey, sleep_for_blocks

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

HEARTBEAT_TIMEOUT = 600  # seconds

def heartbeat_monitor(last_heartbeat, stop_event):
    while not stop_event.is_set():
        time.sleep(5)
        if time.time() - last_heartbeat[0] > HEARTBEAT_TIMEOUT:
            logger.error("No heartbeat detected in the last 600 seconds. Restarting process.")
            logging.shutdown()
            os.execv(sys.executable, [sys.executable] + sys.argv)

@click.command()
@click.option("--network", default=lambda: os.getenv("NETWORK", "finney"), show_default=True,
             help="Network to connect to (finney, test, local).")
@click.option("--netuid", type=int, default=lambda: int(os.getenv("NETUID", "1")), show_default=True,
             help="Subnet netuid.")
@click.option("--coldkey", default=lambda: os.getenv("WALLET_NAME", "default"), show_default=True,
             help="Wallet coldkey name.")
@click.option("--hotkey", default=lambda: os.getenv("HOTKEY_NAME", "default"), show_default=True,
             help="Wallet hotkey name (validator hotkey).")
@click.option("--envelope-hotkey", default=lambda: os.getenv("ENVELOPE_HOTKEY_SS58", ENVELOPE_HOTKEY_SS58),
             help="SS58 hotkey of The Envelope Room (preferred).")
@click.option("--envelope-uid", default=lambda: os.getenv("ENVELOPE_UID", ENVELOPE_UID),
             help="UID of The Envelope Room (optional override; if set, skips lookup).")
@click.option("--dry-run/--live", default=False, show_default=True,
             help="Dry-run logs intended weights without setting on-chain.")
@click.option("--log-level", type=click.Choice(["DEBUG","INFO","WARNING","ERROR"], case_sensitive=False),
             default=lambda: os.getenv("LOG_LEVEL", "INFO"), show_default=True)
def main(network: str, netuid: int, coldkey: str, hotkey: str,
         envelope_hotkey: str, envelope_uid: str, dry_run: bool, log_level: str):
    """Run the Taofather validator."""
    logging.getLogger().setLevel(getattr(logging, log_level.upper()))
    logger.info(f"Starting Taofather validator on network={network}, netuid={netuid}")

    # Heartbeat setup
    last_heartbeat = [time.time()]
    stop_event = threading.Event()
    heartbeat_thread = threading.Thread(target=heartbeat_monitor, args=(last_heartbeat, stop_event), daemon=True)
    heartbeat_thread.start()

    try:
        wallet = Wallet(name=coldkey, hotkey=hotkey)
        subtensor = bt.Subtensor(network=network)
        metagraph = bt.Metagraph(netuid=netuid, network=network)
        metagraph.sync(subtensor=subtensor)
        logger.info(f"Metagraph synced: {metagraph.n} neurons at block {metagraph.block}")

        # Resolve Envelope Room UID
        resolved_uid = None
        if envelope_uid:
            try:
                resolved_uid = int(envelope_uid)
            except ValueError:
                raise SystemExit(f"--envelope-uid must be an int, got: {envelope_uid!r}")

        if resolved_uid is None:
            resolved_uid = find_uid_by_hotkey(metagraph, envelope_hotkey)

        if resolved_uid is None:
            raise SystemExit(
                f"Could not resolve {ENVELOPE_ROOM_NAME} UID. Provide --envelope-hotkey (SS58) or --envelope-uid."
            )

        if not (0 <= resolved_uid < metagraph.n):
            raise SystemExit(f"Envelope Room UID {resolved_uid} is out of range (0..{metagraph.n-1}).")

        logger.info(f"{ENVELOPE_ROOM_NAME} UID resolved to {resolved_uid}")

        # Get our UID (optional, mostly for sanity)
        my_hotkey = wallet.hotkey.ss58_address
        if my_hotkey in metagraph.hotkeys:
            my_uid = metagraph.hotkeys.index(my_hotkey)
            logger.info(f"Validator UID: {my_uid}")
        else:
            logger.warning(f"Validator hotkey {my_hotkey} not registered on netuid {netuid}. "
                           "You can still run, but set_weights will likely fail.")

        # Tempo
        tempo = subtensor.get_subnet_hyperparameters(netuid).tempo
        logger.info(f"Subnet tempo: {tempo} blocks")
        last_weight_block = 0

        while True:
            try:
                metagraph.sync(subtensor=subtensor)
                current_block = subtensor.get_current_block()

                # Heartbeat
                last_heartbeat[0] = time.time()

                blocks_since_last = current_block - last_weight_block
                if blocks_since_last >= tempo:
                    uids = [resolved_uid]
                    weights = [1.0]

                    logger.info(
                        f"Block {current_block}: Setting weights -> 100% to {ENVELOPE_ROOM_NAME} (uid={resolved_uid})"
                    )

                    if dry_run:
                        logger.info("[DRY-RUN] Would call subtensor.set_weights(...)")
                        last_weight_block = current_block
                    else:
                        success = subtensor.set_weights(
                            wallet=wallet,
                            netuid=netuid,
                            uids=uids,
                            weights=weights,
                            wait_for_inclusion=True,
                            wait_for_finalization=False,
                        )
                        if success:
                            logger.info("Successfully set weights.")
                            last_weight_block = current_block
                        else:
                            logger.warning("Failed to set weights (set_weights returned False).")
                else:
                    logger.debug(f"Block {current_block}: Waiting ({blocks_since_last}/{tempo} blocks)")

                sleep_for_blocks(12.0, 1)

            except KeyboardInterrupt:
                logger.info("Validator stopped by user")
                break
            except Exception as e:
                logger.exception(f"Error in validator loop: {e}")
                sleep_for_blocks(12.0, 1)

    finally:
        stop_event.set()
        heartbeat_thread.join(timeout=2)

if __name__ == "__main__":
    main()
