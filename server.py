import os
import subprocess
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()


class WorkflowRequest(BaseModel):
    platform: str
    timeframe: str
    ascent_email: str = None
    ascent_password: str = None
    jobflo_email: str = None
    jobflo_password: str = None
    openai_api_key: str = None
    user_id: str = None


@app.get("/")
def root():
    return {"status": "ok", "service": "crm-workflow-runner"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/run-workflow")
def run_workflow(request: WorkflowRequest):
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

    try:
        result = subprocess.run(
            ["python", "workflow_runner.py"],
            env=env,
            capture_output=True,
            text=True,
            timeout=1800
        )

        if result.returncode != 0:
            raise HTTPException(
                status_code=500,
                detail=f"Workflow failed: {result.stderr}"
            )

        return {
            "status": "success",
            "output": result.stdout
        }

    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=504, detail="Workflow timed out")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
