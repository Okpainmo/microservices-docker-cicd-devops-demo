# Microservices Job Queue Demo

This project is a multi-service job processing system designed to demonstrate containerization and CI/CD best practices.

## Services

- **Frontend**: Node.js/Express app for job submission and tracking.
- **API**: Python/FastAPI backend for job management.
- **Worker**: Python worker that processes jobs from the Redis queue.
- **Redis**: Shared queue and state store.

## Prerequisites

- Docker
- Docker Compose

## Getting Started

1. **Clone the repository**:

   ```bash
   git clone https://github.com/Okpainmo/microservices-docker-cicd-devops-demo
   cd microservices-docker-cicd-devops-demo
   ```

2. **Configure environment variables**:

   Copy the example environment file and adjust if necessary:

   ```bash
   cp .env.example .env
   ```

3. **Bring up the stack**:

   ```bash
   docker-compose up -d --build
   ```

4. **Verify startup**:

   Wait for all services to become healthy. You can check the status with:
   
   ```bash
   docker-compose ps
   ```
   A successful startup will show all services as `Up (healthy)`.

5. **Access the application**:

   Open your browser at `http://localhost:3000` (or the port defined in `.env`).

## CI/CD Pipeline

The project uses separated GitHub Actions workflows for better modularity:

### CI Pipeline (`ci.yml`)

Runs on all pull requests and pushes to `main`:

1. **Linting**: `flake8` (Python), `eslint` (JS), and `hadolint` (Dockerfiles).
2. **Unit Testing**: `pytest` with coverage reporting.
3. **Container Building**: Multi-stage Docker builds.
4. **Security Scanning**: `Trivy` image scanning for CRITICAL vulnerabilities.
5. **Integration Testing**: Full stack deployment and end-to-end job processing check.

### CD Pipeline (`cd.yml`)

Triggered automatically after a successful CI run on the `main` branch:

1. **Deployment**: Performs a scripted **rolling update** (zero-downtime) by scaling the API service, verifying health, and decommissioning old containers.

## Documentation

- `FIXES.md`: Detailed log of bug fixes in the application code.
- `.env.example`: Template for required environment variables.
