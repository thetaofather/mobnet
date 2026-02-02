from __future__ import annotations
from typing import Literal, Optional, List
from pydantic import BaseModel, Field

JobKind = Literal["hit", "racket"]
JobStatus = Literal["open", "armed", "refund", "executed", "closed"]

class Participant(BaseModel):
    ss58: str
    amount_planck: int = 0  # 1e9 planck = 1 TAO

class JobTerms(BaseModel):
    title: str
    kind: JobKind
    target_netuid: int
    target_hotkey: Optional[str] = None
    theta_refund: float = 0.4
    theta_full: float = 0.9
    capacity_planck: int = 0
    dispute_delay_blocks: int = 100

class JobOnChain(BaseModel):
    job_id: str
    created_at: str
    status: JobStatus
    boss_ss58: str
    escrow_address: str
    terms: JobTerms
    participants: List[Participant] = Field(default_factory=list)
    manifest_sha256: str

class LocalVerdict(BaseModel):
    job_id: str
    validator_hotkey: str
    validator_uid: int
    observed_block: int
    ok_to_execute: bool
    reason: str = ""
