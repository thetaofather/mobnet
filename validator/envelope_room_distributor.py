"""Envelope Room Distributor

Sets validator weights so 100% of miner emissions route to the Envelope Room UID.
"""

from __future__ import annotations
import logging
from typing import List, Tuple
import bittensor as bt

logger = logging.getLogger("envelope_room_distributor")

def build_envelope_room_weights(envelope_room_uid: int) -> Tuple[List[int], List[float]]:
    return [int(envelope_room_uid)], [1.0]

def set_envelope_room_weights(wallet: "bt.wallet", subtensor: "bt.subtensor", netuid: int, envelope_room_uid: int) -> bool:
    uids, weights = build_envelope_room_weights(envelope_room_uid)
    logger.info(f"Setting 100% weights to Envelope Room UID={envelope_room_uid} on netuid={netuid}")
    ok = subtensor.set_weights(
        wallet=wallet,
        netuid=netuid,
        uids=uids,
        weights=weights,
        wait_for_inclusion=True,
        wait_for_finalization=False,
    )
    return bool(ok)
