from __future__ import annotations
import json, hashlib
from typing import Any
from jobs.models import JobOnChain

def canonical_json(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)

def compute_manifest_sha256(job: JobOnChain) -> str:
    payload = {
        "job_id": job.job_id,
        "created_at": job.created_at,
        "boss_ss58": job.boss_ss58,
        "escrow_address": job.escrow_address,
        "terms": job.terms.model_dump(),
    }
    raw = canonical_json(payload).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()
