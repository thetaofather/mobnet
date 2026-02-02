"""Taofather Validator (Testnet Scaffold)

1) Set weights to route emissions to the Envelope Room UID.
2) Poll Job Board, verify jobs, and execute payouts after stake-majority consensus + dispute delay.
"""

from __future__ import annotations

import os, sys, time, logging, threading
import click
import bittensor as bt

from validator.envelope_room_distributor import set_envelope_room_weights
from jobs.watcher import JobWatcher, WatcherConfig

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("validator")

HEARTBEAT_TIMEOUT = 600

def heartbeat_monitor(last_heartbeat, stop_event):
    while not stop_event.is_set():
        time.sleep(5)
        if time.time() - last_heartbeat[0] > HEARTBEAT_TIMEOUT:
            logger.error("No heartbeat detected. Restarting process.")
            try:
                import logging as _logging
                _logging.shutdown()
            finally:
                os.execv(sys.executable, [sys.executable] + sys.argv)

@click.command()
@click.option("--network", default=lambda: os.getenv("NETWORK", "test"), help="finney | test | local")
@click.option("--netuid", type=int, default=lambda: int(os.getenv("NETUID", "9999")))
@click.option("--coldkey", default=lambda: os.getenv("WALLET_NAME", "default"))
@click.option("--hotkey", default=lambda: os.getenv("HOTKEY_NAME", "default"))
@click.option("--envelope-room-uid", type=int, default=lambda: int(os.getenv("ENVELOPE_ROOM_UID", "0")))
@click.option("--job-board-url", default=lambda: os.getenv("JOB_BOARD_URL", "http://127.0.0.1:8088"))
@click.option("--log-level", type=click.Choice(["DEBUG","INFO","WARNING","ERROR"], case_sensitive=False),
              default=lambda: os.getenv("LOG_LEVEL","INFO"))
def main(network: str, netuid: int, coldkey: str, hotkey: str, envelope_room_uid: int, job_board_url: str, log_level: str):
    logging.getLogger().setLevel(getattr(logging, log_level.upper()))
    logger.info(f"Starting Taofather validator network={network} netuid={netuid}")

    last_heartbeat = [time.time()]
    stop_event = threading.Event()
    threading.Thread(target=heartbeat_monitor, args=(last_heartbeat, stop_event), daemon=True).start()

    wallet = bt.wallet(name=coldkey, hotkey=hotkey)
    subtensor = bt.subtensor(network=network)
    metagraph = bt.metagraph(netuid=netuid, network=network)
    metagraph.sync(subtensor=subtensor)

    my_hotkey = wallet.hotkey.ss58_address
    if my_hotkey not in metagraph.hotkeys:
        logger.error(f"Hotkey {my_hotkey} not registered on netuid {netuid}")
        return
    my_uid = metagraph.hotkeys.index(my_hotkey)
    logger.info(f"Validator UID={my_uid}")

    tempo = subtensor.get_subnet_hyperparameters(netuid).tempo
    logger.info(f"Subnet tempo={tempo} blocks")

    cfg = WatcherConfig(
        network=network,
        netuid=netuid,
        job_board_url=job_board_url.rstrip("/"),
        dispute_delay_blocks=int(os.getenv("DISPUTE_DELAY_BLOCKS","100")),
        consensus_stake_fraction=float(os.getenv("CONSENSUS_STAKE_FRACTION","0.51")),
        envelope_room_uid=envelope_room_uid,
    )
    watcher = JobWatcher(cfg=cfg, wallet=wallet, subtensor=subtensor, metagraph=metagraph, my_uid=my_uid)

    last_weight_block = 0
    try:
        while True:
            metagraph.sync(subtensor=subtensor)
            current_block = subtensor.get_current_block()
            last_heartbeat[0] = time.time()

            if current_block - last_weight_block >= tempo:
                if set_envelope_room_weights(wallet, subtensor, netuid, envelope_room_uid):
                    last_weight_block = current_block
                    logger.info("Weights updated (Envelope Room routing).")

            watcher.tick(current_block=current_block)
            time.sleep(12)
    except KeyboardInterrupt:
        logger.info("Stopped.")
    finally:
        stop_event.set()

if __name__ == "__main__":
    main()
