from __future__ import annotations
import hashlib
from typing import List
from scalecodec.utils.ss58 import ss58_encode, ss58_decode

MULTISIG_PALLET_ID = b"modlpy/utilisuba"  # 16 bytes

def _compact_u32(n: int) -> bytes:
    if n < 1 << 6:
        return bytes([(n << 2) & 0xFF])
    raise ValueError("compact encoding for large values not implemented")

def multisig_address(signatories: List[str], threshold: int, ss58_format: int = 42) -> str:
    """Derive a multisig account address (pallet-multisig multi_account_id)."""
    if threshold <= 0 or threshold > len(signatories):
        raise ValueError("invalid threshold")
    ids = [bytes.fromhex(ss58_decode(s)) for s in signatories]
    ids = sorted(ids)

    payload = bytearray()
    payload += MULTISIG_PALLET_ID
    payload += _compact_u32(len(ids))
    for b in ids:
        payload += b
    payload += int(threshold).to_bytes(2, "little")
    account_id = hashlib.blake2b(bytes(payload), digest_size=32).digest()
    return ss58_encode(account_id, ss58_format=ss58_format)
