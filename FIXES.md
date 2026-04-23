# Bug Fixes

This document tracks all bugs found in the original application and the fixes applied to make it production-ready.

| File               | Line   | Issue                                                                                        | Fix                                                                                        |
| ------------------ | ------ | -------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| `api/main.py`      | 8      | Hardcoded Redis host (`localhost`) prevents service discovery in Docker.                     | Use `REDIS_HOST` environment variable with a default fallback.                             |
| `api/main.py`      | 8      | Redis connection lacks `decode_responses=True`, causing issues with byte/string conversions. | Enabled `decode_responses=True` in the Redis client initialization.                        |
| `api/main.py`      | 15-24  | `create_job` lacks error handling for Redis connection failures.                             | Added `try-except` block to catch `redis.ConnectionError` and return a 503 status.         |
| `api/main.py`      | 26-35  | `get_job` returns 200 OK even if a job is not found in Redis.                                | Added check for empty `job_data` and raised a 404 `HTTPException`.                         |
| `api/main.py`      | 33-34  | Manual byte decoding (`.decode()`) is prone to errors if data is already decoded or missing. | Relied on `decode_responses=True` and used `.get()` with defaults for safer access.        |
| `api/main.py`      | N/A    | Missing health check endpoint for container orchestration.                                   | Added `@app.get("/health")` endpoint.                                                      |
| `worker/worker.py` | 6      | Hardcoded Redis host (`localhost`) prevents connection within Docker network.                | Use `REDIS_HOST` environment variable.                                                     |
| `worker/worker.py` | 6      | Redis connection lacks `decode_responses=True`.                                              | Enabled `decode_responses=True`.                                                           |
| `worker/worker.py` | 11     | `r.hset` doesn't handle connection errors, potentially crashing the worker.                  | Added error handling around Redis operations.                                              |
| `worker/worker.py` | 14-18  | Worker crashes on Redis connection loss; no retry logic.                                     | Implemented a retry loop with a 5-second delay on connection errors.                       |
| `worker/worker.py` | 18     | `job_id.decode()` fails if Redis is configured to decode responses automatically.            | Removed redundant `.decode()` call.                                                        |
| `worker/worker.py` | N/A    | Worker lacks graceful shutdown handling for `SIGTERM`.                                       | Added signal handlers to ensure clean exit.                                                |
| `frontend/app.js`  | 18, 27 | Generic 500 error messages hide root causes from developers.                                 | Updated to log actual error messages and return more specific status codes where possible. |
| `frontend/app.js`  | 15, 24 | API calls lack timeouts, potentially hanging frontend requests.                              | Added a 5-second timeout to all `axios` requests.                                          |
| Multiple           | N/A    | Services run as `root` user by default.                                                      | Created non-root `appuser` in all Dockerfiles and switched with `USER` instruction.        |
| Multiple           | N/A    | Missing `HEALTHCHECK` instructions in Dockerfiles.                                           | Added service-specific health checks (Python/Node/Redis-cli).                              |
| Docker             | N/A    | Redis exposed on host and lacks resource limits.                                             | Removed port mapping for Redis and added CPU/Memory limits to `docker-compose.yml`.        |
