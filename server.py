import os
import uuid
import subprocess
import threading
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# In-memory job store
jobs = {}


class WorkflowRequest(BaseModel):
    platform: str
    timeframe: str
    ascent_email: str = None
    ascent_password: str = None
    jobflo_email: str = None
    jobflo_password: str = None
    openai_api_key: str = None
    user_id: str = None


def run_workflow_thread(job_id: str, env: dict):
    try:
        jobs[job_id]["status"] = "running"
        result = subprocess.run(
            ["python", "workflow_runner.py"],
            env=env,
            capture_output=True,
            text=True,
            timeout=1800
        )
        if result.returncode != 0:
            jobs[job_id]["status"] = "error"
            jobs[job_id]["error"] = result.stderr
        else:
            jobs[job_id]["status"] = "complete"
            jobs[job_id]["output"] = result.stdout
    except subprocess.TimeoutExpired:
        jobs[job_id]["status"] = "error"
        jobs[job_id]["error"] = "Workflow timed out"
    except Exception as e:
        jobs[job_id]["status"] = "error"
        jobs[job_id]["error"] = str(e)


@app.get("/")
def root():
    return {"status": "ok", "service": "crm-workflow-runner"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/start-workflow")
def start_workflow(request: WorkflowRequest):
    platform = request.platform.lower()

    if platform not in ["ascent", "jobflo"]:
        raise HTTPException(status_code=400, detail="Invalid platform")

    env = os.environ.copy()

    if request.openai_api_key:
        env["OPENAI_API_KEY"] = request.openai_api_key

    if platform == "ascent":
        if not request.ascent_email or not request.ascent_password:
            raise HTTPException(status_code=400, detail="Ascent credentials required")
        env["ASCENT_EMAIL"] = request.ascent_email
        env["ASCENT_PASSWORD"] = request.ascent_password

    elif platform == "jobflo":
        if not request.jobflo_email or not request.jobflo_password:
            raise HTTPException(status_code=400, detail="JobFlo credentials required")
        env["JOBFLO_EMAIL"] = request.jobflo_email
        env["JOBFLO_PASSWORD"] = request.jobflo_password

    env["WORKFLOW_PLATFORM"] = platform
    env["WORKFLOW_TIMEFRAME"] = request.timeframe
    env["WORKFLOW_USER_ID"] = request.user_id or ""

    job_id = str(uuid.uuid4())
    jobs[job_id] = {"status": "pending", "output": None, "error": None}

    thread = threading.Thread(target=run_workflow_thread, args=(job_id, env))
    thread.daemon = True
    thread.start()

    return {"job_id": job_id, "status": "pending"}


@app.get("/job-status/{job_id}")
def job_status(job_id: str):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    return jobs[job_id]


# Keep old endpoint for compatibility
@app.post("/run-workflow")
def run_workflow(request: WorkflowRequest):
    return start_workflow(request)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
