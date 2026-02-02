from __future__ import annotations

import os, json, uuid, time
from pathlib import Path
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, JSONResponse

from jobs.models import JobOnChain, JobTerms, Participant
from jobs.manifest import compute_manifest_sha256

app = FastAPI(title="Taofather Private Job Board")

STATE = Path(os.getenv("PRIVATE_STATE_DIR", "./private_state"))
STATE.mkdir(parents=True, exist_ok=True)
JOBS_PATH = STATE / "jobs.json"

def _load_jobs():
    if JOBS_PATH.exists():
        return json.loads(JOBS_PATH.read_text(encoding="utf-8"))
    return []

def _save_jobs(jobs):
    JOBS_PATH.write_text(json.dumps(jobs, indent=2, sort_keys=True), encoding="utf-8")

FORM_HTML = """<!doctype html>
<html>
<head><meta charset='utf-8'><title>Taofather Job Submission</title></head>
<body style='font-family:sans-serif;max-width:900px;margin:2rem auto;'>
<h1>Boss Job Submission (Private)</h1>
<p>Local testing only. Keep this private (it is gitignored).</p>

<form method='post' action='/submit'>
  <label>Boss SS58<br><input name='boss_ss58' style='width:100%'></label><br><br>
  <label>Title<br><input name='title' style='width:100%'></label><br><br>

  <label>Kind
    <select name='kind'>
      <option value='hit'>hit (sell → TAO payouts)</option>
      <option value='racket'>racket (buy/stake → alpha credits)</option>
    </select>
  </label><br><br>

  <label>Target netuid<br><input name='target_netuid' value='1'></label><br><br>
  <label>Escrow address (deposit address)<br><input name='escrow_address' style='width:100%'></label><br><br>
  <label>Dispute delay (blocks)<br><input name='dispute_delay_blocks' value='100'></label><br><br>

  <h3>Participants JSON</h3>
  <p>Example:</p>
  <pre>[
  {"ss58":"5F...","amount_planck":1000000000},
  {"ss58":"5G...","amount_planck":2000000000}
]</pre>
  <textarea name='participants_json' style='width:100%;height:180px;'></textarea><br><br>

  <button type='submit'>Create Job</button>
</form>
</body>
</html>"""

@app.get("/", response_class=HTMLResponse)
def home():
    return FORM_HTML

@app.get("/jobs")
def list_jobs():
    return _load_jobs()

@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    for j in _load_jobs():
        if j.get("job_id") == job_id:
            return j
    return JSONResponse({"error":"not found"}, status_code=404)

@app.post("/submit")
def submit(
    boss_ss58: str = Form(...),
    title: str = Form(...),
    kind: str = Form(...),
    target_netuid: int = Form(...),
    escrow_address: str = Form(...),
    dispute_delay_blocks: int = Form(100),
    participants_json: str = Form("[]"),
):
    try:
        participants_raw = json.loads(participants_json or "[]")
    except Exception:
        participants_raw = []

    job_id = uuid.uuid4().hex[:12]
    terms = JobTerms(
        title=title,
        kind=kind,
        target_netuid=int(target_netuid),
        dispute_delay_blocks=int(dispute_delay_blocks),
    )

    job = JobOnChain(
        job_id=job_id,
        created_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        status="armed",
        boss_ss58=boss_ss58,
        escrow_address=escrow_address,
        terms=terms,
        participants=[Participant(**p) for p in participants_raw],
        manifest_sha256="",
    )
    job.manifest_sha256 = compute_manifest_sha256(job)

    jobs = _load_jobs()
    jobs.append(job.model_dump())
    _save_jobs(jobs)

    return {"ok": True, "job_id": job_id, "manifest_sha256": job.manifest_sha256, "escrow_address": escrow_address}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8088)
