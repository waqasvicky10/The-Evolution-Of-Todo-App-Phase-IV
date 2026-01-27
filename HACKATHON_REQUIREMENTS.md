# Hackathon II - Complete Requirements Document
## The Evolution of Todo – Mastering Spec-Driven Development & Cloud Native AI

**Source:** Official Hackathon Document
**Date:** 2026-01-24
**Status:** Active

---

## Overview

This hackathon teaches the **Nine Pillars of AI-Driven Development** through building a Todo app that evolves from a simple console app to a fully-featured, cloud-native AI chatbot deployed on Kubernetes.

**Key Learning:**
- Spec-Driven Development using Claude Code and Spec-Kit Plus
- Reusable Intelligence: Agents Skills and Subagent Development
- Full-Stack Development with Next.js, FastAPI, SQLModel, and Neon Serverless Database
- AI Agent Development using OpenAI Agents SDK and Official MCP SDK
- Cloud-Native Deployment with Docker, Kubernetes, Minikube, and Helm Charts
- Event-Driven Architecture using Kafka and Dapr
- AIOps with kubectl-ai, kagent and Claude Code

---

## Phase Breakdown

### Phase I: Todo In-Memory Python Console App
**Points:** 100 | **Due:** Dec 7, 2025

**Objective:** Build a command-line todo application that stores tasks in memory using Claude Code and Spec-Kit Plus.

**Requirements:**
- Implement all 5 Basic Level features (Add, Delete, Update, View, Mark Complete)
- Use spec-driven development with Claude Code and Spec-Kit Plus
- Follow clean code principles and proper Python project structure

**Technology Stack:**
- UV
- Python 3.13+
- Claude Code
- Spec-Kit Plus

**Deliverables:**
1. GitHub repository with:
   - Constitution file
   - specs history folder containing all specification files
   - /src folder with Python source code
   - README.md with setup instructions
   - CLAUDE.md with Claude Code instructions

2. Working console application demonstrating:
   - Adding tasks with title and description
   - Listing all tasks with status indicators
   - Updating task details
   - Deleting tasks by ID
   - Marking tasks as complete/incomplete

---

### Phase II: Todo Full-Stack Web Application
**Points:** 150 | **Due:** Dec 14, 2025

**Objective:** Transform the console app into a modern multi-user web application with persistent storage.

**Requirements:**
- Implement all 5 Basic Level features as a web application
- Create RESTful API endpoints
- Build responsive frontend interface
- Store data in Neon Serverless PostgreSQL database
- Authentication – Implement user signup/signin using Better Auth

**Technology Stack:**
- Frontend: Next.js 16+ (App Router)
- Backend: Python FastAPI
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth

**API Endpoints:**
- GET `/api/{user_id}/tasks` - List all tasks
- POST `/api/{user_id}/tasks` - Create a new task
- GET `/api/{user_id}/tasks/{id}` - Get task details
- PUT `/api/{user_id}/tasks/{id}` - Update a task
- DELETE `/api/{user_id}/tasks/{id}` - Delete a task
- PATCH `/api/{user_id}/tasks/{id}/complete` - Toggle completion

**Security:**
- Better Auth + FastAPI Integration
- JWT tokens for authentication
- User data isolation (users only see their own tasks)

---

### Phase III: Todo AI Chatbot
**Points:** 200 | **Due:** Dec 21, 2025

**Objective:** Create an AI-powered chatbot interface for managing todos through natural language using MCP (Model Context Protocol) server architecture.

**Requirements:**
1. Implement conversational interface for all Basic Level features
2. Use OpenAI Agents SDK for AI logic
3. Build MCP server with Official MCP SDK that exposes task operations as tools
4. Stateless chat endpoint that persists conversation state to database
5. AI agents use MCP tools to manage tasks

**Technology Stack:**
- Frontend: OpenAI ChatKit
- Backend: Python FastAPI
- AI Framework: OpenAI Agents SDK
- MCP Server: Official MCP SDK
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth

**Architecture:**
```
ChatKit UI → FastAPI Chat Endpoint → OpenAI Agents SDK → MCP Server → Neon DB
```

**MCP Tools Required:**
1. `add_task` - Create a new task
2. `list_tasks` - Retrieve tasks from the list
3. `complete_task` - Mark a task as complete
4. `delete_task` - Remove a task from the list
5. `update_task` - Modify task title or description

**Database Models:**
- Task (user_id, id, title, description, completed, created_at, updated_at)
- Conversation (user_id, id, created_at, updated_at)
- Message (user_id, id, conversation_id, role, content, created_at)

**Chat API Endpoint:**
- POST `/api/{user_id}/chat` - Send message & get AI response

**Natural Language Commands:**
- "Add a task to buy groceries" → `add_task`
- "Show me all my tasks" → `list_tasks`
- "Mark task 3 as complete" → `complete_task`
- "Delete the meeting task" → `delete_task`
- "Change task 1 to 'Call mom tonight'" → `update_task`

**Bonus Features:**
- Multi-language Support (Urdu) - +100 points
- Voice Commands - +200 points

---

### Phase IV: Local Kubernetes Deployment
**Points:** 250 | **Due:** Jan 4, 2026

**Objective:** Deploy the Todo Chatbot on a local Kubernetes cluster using Minikube, Helm Charts.

**Requirements:**
- Containerize frontend and backend applications (Use Gordon)
- Use Docker AI Agent (Gordon) for AI-assisted Docker operations
- Create Helm charts for deployment (Use kubectl-ai and/or kagent to generate)
- Use kubectl-ai and kagent for AI-assisted Kubernetes operations
- Deploy on Minikube locally

**Technology Stack:**
- Containerization: Docker (Docker Desktop)
- Docker AI: Docker AI Agent (Gordon)
- Orchestration: Kubernetes (Minikube)
- Package Manager: Helm Charts
- AI DevOps: kubectl-ai, Kagent
- Application: Phase III Todo Chatbot

**AIOps Tools:**
- Docker AI Agent (Gordon) for intelligent Docker operations
- kubectl-ai for intelligent Kubernetes operations
- Kagent for advanced Kubernetes management

---

### Phase V: Advanced Cloud Deployment
**Points:** 300 | **Due:** Jan 18, 2026

**Objective:** Implement advanced features and deploy to production-grade Kubernetes on Azure/Google Cloud/Oracle and Kafka within Kubernetes Cluster.

**Part A: Advanced Features**
- Implement all Advanced Level features (Recurring Tasks, Due Dates & Reminders)
- Implement Intermediate Level features (Priorities, Tags, Search, Filter, Sort)
- Add event-driven architecture with Kafka
- Implement Dapr for distributed application runtime

**Part B: Local Deployment**
- Deploy to Minikube
- Deploy Dapr on Minikube use Full Dapr: Pub/Sub, State, Bindings (cron), Secrets, Service Invocation

**Part C: Cloud Deployment**
- Deploy to Azure (AKS)/Google Cloud (GKE)/Oracle (OKE)
- Deploy Dapr on GKE/AKS use Full Dapr: Pub/Sub, State, Bindings (cron), Secrets, Service Invocation
- Use Kafka on Confluent/Redpanda Cloud
- Set up CI/CD pipeline using Github Actions
- Configure monitoring and logging

**Technology Stack:**
- Cloud K8s: Azure AKS / Google GKE / Oracle OKE
- Event Streaming: Kafka (Redpanda Cloud / Strimzi)
- Distributed Runtime: Dapr
- CI/CD: GitHub Actions

**Kafka Use Cases:**
1. Reminder/Notification System
2. Recurring Task Engine
3. Activity/Audit Log
4. Real-time Sync Across Clients

**Dapr Building Blocks:**
1. Pub/Sub (Kafka abstraction)
2. State Management (Conversation state storage)
3. Service Invocation (Frontend → Backend communication)
4. Bindings (Cron triggers for scheduled reminders)
5. Secrets Management (Store API keys, DB credentials securely)

**Cloud Options:**
- **Oracle Cloud (Recommended):** Always free (4 OCPUs, 24GB RAM)
- **Azure AKS:** $200 credits for 30 days
- **Google GKE:** $300 credits for 90 days

---

## Bonus Points

| Feature | Points |
|---------|--------|
| Reusable Intelligence – Create and use reusable intelligence via Claude Code Subagents and Agent Skills | +200 |
| Create and use Cloud-Native Blueprints via Agent Skills | +200 |
| Multi-language Support – Support Urdu in chatbot | +100 |
| Voice Commands – Add voice input for todo commands | +200 |
| **TOTAL BONUS** | **+600** |

---

## Submission Requirements

**For Each Phase:**
1. Public GitHub Repo Link
2. Published App Link for Vercel
3. Demo video link (must be under 90 seconds)
4. WhatsApp number (for presentation invitation)

**Required Submissions:**
1. Public GitHub Repository containing:
   - All source code for all completed phases
   - /specs folder with all specification files
   - CLAUDE.md with Claude Code instructions
   - README.md with comprehensive documentation
   - Clear folder structure for each phase

2. Deployed Application Links:
   - Phase II: Vercel/frontend URL + Backend API URL
   - Phase III-V: Chatbot URL
   - Phase IV: Instructions for local Minikube setup
   - Phase V: DigitalOcean deployment URL

3. Demo Video (maximum 90 seconds):
   - Demonstrate all implemented features
   - Show spec-driven development workflow
   - Judges will only watch the first 90 seconds

---

## Timeline

| Milestone | Date | Description |
|-----------|------|-------------|
| Hackathon Start | Monday, Dec 1, 2025 | Documentation released |
| Phase I Due | Sunday, Dec 7, 2025 | Console app checkpoint |
| Phase II Due | Sunday, Dec 14, 2025 | Web app checkpoint |
| Phase III Due | Sunday, Dec 21, 2025 | Chatbot checkpoint |
| Phase IV Due | Sunday, Jan 4, 2026 | Local K8s checkpoint |
| Final Submission | Sunday, Jan 18, 2026 | All phases complete |
| Live Presentations | Sundays, Dec 7, 14, 21, and Jan 4 and 18 | Top submissions present |

---

## Key Requirements

### Spec-Driven Development (MANDATORY)
- You must implement all 5 Phases using Spec-Driven Development
- Write a Markdown Constitution and Spec for every feature
- Use Claude Code to generate the implementation
- **Constraint:** You cannot write the code manually. You must refine the Spec until Claude Code generates the correct output.

### Agentic Dev Stack Workflow
1. Write spec → Generate plan → Break into tasks → Implement via Claude Code
2. No manual coding allowed
3. Process, prompts, and iterations will be reviewed for judging

### Technology Constraints
- Core stack must remain as specified
- Can add additional tools/libraries
- Must follow approved technologies per phase

---

## Resources

### Core Tools
- Claude Code: claude.com/product/claude-code
- GitHub Spec-Kit: github.com/panaversity/spec-kit-plus
- OpenAI ChatKit: platform.openai.com/docs/guides/chatkit
- MCP: github.com/modelcontextprotocol/python-sdk

### Infrastructure
- Neon DB: neon.tech (Free tier available)
- Vercel: vercel.com (Free frontend hosting)
- DigitalOcean: digitalocean.com ($200 credit for 60 days)
- Minikube: minikube.sigs.k8s.io (Local Kubernetes)

---

## Total Points

| Phase | Points |
|-------|--------|
| Phase I | 100 |
| Phase II | 150 |
| Phase III | 200 |
| Phase IV | 250 |
| Phase V | 300 |
| Bonus | +600 |
| **TOTAL** | **1,000 + 600 bonus** |

---

**END OF HACKATHON REQUIREMENTS**
