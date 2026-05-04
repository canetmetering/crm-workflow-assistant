import os
import uuid
import subprocess
import threading
import queue
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

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
    q = jobs[job_id]["queue"]
    try:
        jobs[job_id]["status"] = "running"
        process = subprocess.Popen(
            ["python", "workflow_runner.py"],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        for line in process.stdout:
            line = line.strip()
            if line:
                jobs[job_id]["lines"].append(line)
                q.put({"type": "line", "text": line})

        process.wait()

        if process.returncode != 0:
            err = process.stderr.read()
            jobs[job_id]["status"] = "error"
            jobs[job_id]["error"] = err
            q.put({"type": "error", "text": err})
        else:
            jobs[job_id]["status"] = "complete"
            q.put({"type": "complete", "text": "Workflow complete."})

    except Exception as e:
        jobs[job_id]["status"] = "error"
        jobs[job_id]["error"] = str(e)
        q.put({"type": "error", "text": str(e)})
    finally:
        q.put(None)  # sentinel to close stream


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
    jobs[job_id] = {
        "status": "pending",
        "lines": [],
        "error": None,
        "queue": queue.Queue()
    }

    thread = threading.Thread(target=run_workflow_thread, args=(job_id, env))
    thread.daemon = True
    thread.start()

    return {"job_id": job_id, "status": "pending"}


@app.get("/stream-job/{job_id}")
def stream_job(job_id: str):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")

    def event_stream():
        q = jobs[job_id]["queue"]
        # Send any lines already collected
        for line in jobs[job_id]["lines"]:
            yield f"data: {line}\n\n"

        while True:
            item = q.get()
            if item is None:
                yield "data: __DONE__\n\n"
                break
            if item["type"] == "error":
                yield f"data: __ERROR__ {item['text']}\n\n"
                break
            yield f"data: {item['text']}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")


@app.get("/job-status/{job_id}")
def job_status(job_id: str):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    job = jobs[job_id]
    return {
        "status": job["status"],
        "lines": job["lines"],
        "error": job["error"]
    }


@app.post("/run-workflow")
def run_workflow(request: WorkflowRequest):
    return start_workflow(request)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
