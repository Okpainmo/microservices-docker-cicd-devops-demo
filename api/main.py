import os
from fastapi import FastAPI, HTTPException
import redis
import uuid
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

class JobRequest(BaseModel):
    title: Optional[str] = None

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/jobs")
def create_job(job: JobRequest):
    job_id = str(uuid.uuid4())
    try:
        r.lpush("job", job_id)
        r.hset(f"job:{job_id}", mapping={
            "status": "queued",
            "title": job.title or "Untitled Job"
        })
    except redis.ConnectionError:
        raise HTTPException(status_code=503, detail="Redis connection failed")
    
    return {"job_id": job_id}

@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    try:
        job_data = r.hgetall(f"job:{job_id}")
    except redis.ConnectionError:
        raise HTTPException(status_code=503, detail="Redis connection failed")

    if not job_data:
        raise HTTPException(status_code=404, detail="Job not found")
        
    return {
        "job_id": job_id, 
        "status": job_data.get("status", "unknown"),
        "title": job_data.get("title", "Untitled Job")
    }
