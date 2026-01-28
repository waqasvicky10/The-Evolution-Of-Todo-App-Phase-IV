# PHASE IV PLAN: Production Transition
## Goal
Transition the Todo App from a local mock environment (Phase III) to a production-ready, cloud-backed architecture (Phase IV).

## 1. Database Migration (SQLite → Neon PostgreSQL)
**Current Status**: using local `todo.db` (SQLite).
**Target Status**: using Neon Serverless PostgreSQL.

### Implementation Steps:
1.  **Configuration**: Update `backend/.env` with `DATABASE_URL` from Neon.
2.  **Dependencies**: Ensure `psycopg2-binary` is installed.
3.  **Migration**: Run `alembic upgrade head` to create schema in Neon.
4.  **Verification**: Restart backend and verify connections via `/health`.

## 2. Intelligence Upgrade (Mock Agent → Real LLM)
**Current Status**: `MockProvider` uses Regex/Rules for English & Urdu.
**Target Status**: `OpenAIProvider` (or similar) using real LLM for natural language understanding.

### Implementation Steps:
1.  **Enable Provider**: Update `phase_iii/agent/agent.py` to accept `OPENAI_API_KEY`.
2.  **Configuration**: Add `OPENAI_API_KEY` to `backend/.env`.
3.  **Refinement**: Ensure the LLM System Prompt handles the Urdu requirements and Tool definitions correctly.
4.  **Testing**: Verify "fuzzy" commands that Regex missed (e.g., "Add that thing I mentioned earlier").

## 3. Deployment (Local → Cloud)
**Current Status**: Running on `localhost:8000`.
**Target Status**: Deployed to Cloud (Vercel/Railway/K8s).

### Implementation Steps:
1.  **Containerization**: Create `Dockerfile` for Backend and Frontend.
2.  **Orchestration**: Create Kubernetes manifests (Deployment, Service, Ingress).
3.  **CI/CD**: Setup GitHub Actions for automated deployment.

## Execution Checklist
- [ ] Connect Neon Database in `.env`
- [ ] Run Alembic Migrations on Neon
- [ ] Enable OpenAI Provider in `agent.py`
- [ ] Verify End-to-End Chat with Real DB & Real Agent
