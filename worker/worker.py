import redis
import time
import os
import signal
import sys

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

def handle_shutdown(signum, frame):
    print("Shutting down worker...")
    sys.exit(0)

signal.signal(signal.SIGTERM, handle_shutdown)
signal.signal(signal.SIGINT, handle_shutdown)

def process_job(job_id):
    print(f"Processing job {job_id}")
    time.sleep(2)  # simulate work
    try:
        r.hset(f"job:{job_id}", "status", "completed")
        print(f"Done: {job_id}")
    except redis.ConnectionError as e:
        print(f"Failed to update job status in Redis: {e}")

if __name__ == "__main__":
    print(f"Worker started, connecting to Redis at {REDIS_HOST}:{REDIS_PORT}")
    while True:
        try:
            job = r.brpop("job", timeout=5)
            if job:
                _, job_id = job
                process_job(job_id)
        except redis.ConnectionError:
            print("Redis connection lost. Retrying in 5 seconds...")
            time.sleep(5)