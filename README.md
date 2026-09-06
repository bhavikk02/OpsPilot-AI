# OpsPilot AI 🚀

AI-powered DevOps assistant that uses Retrieval-Augmented Generation (RAG) to answer infrastructure and DevOps troubleshooting questions from a curated internal knowledge base.

The application is built with **FastAPI, ChromaDB, Azure OpenAI, Docker, GitHub Actions, Azure Container Registry (ACR), and Azure Container Apps**.

---

## Overview

OpsPilot AI is an internal AI assistant designed for DevOps teams.

Instead of relying only on an LLM's general knowledge, OpsPilot AI first retrieves relevant information from a curated DevOps knowledge base.

A relevance gate then evaluates whether the retrieved information is sufficient to answer the user's question.

If the knowledge is relevant, Azure OpenAI generates the final answer using the retrieved context.

If the knowledge base does not contain enough relevant information, OpsPilot AI refuses to generate an unsupported answer.

This approach helps reduce hallucinations and keeps responses grounded in the available knowledge base.

---

## Key Features

- Retrieval-Augmented Generation (RAG)
- ChromaDB vector database
- Curated DevOps knowledge base
- Azure OpenAI integration
- LLM-based relevance gate
- Grounded answer generation
- Unsupported-question fallback
- Source attribution
- FastAPI REST API
- Input validation
- Structured application logging
- Health endpoint
- Docker containerization
- Docker Compose support
- Container healthcheck
- Automatic container restart
- GitHub Actions CI/CD
- Azure OIDC authentication
- Azure Container Registry
- ACR Repository ABAC permissions
- Managed identity for container image pull
- Azure Container Apps deployment
- Container Apps revisions
- Liveness and readiness probes
- Azure Log Analytics
- Production log querying using KQL

---

# Architecture

## Application Architecture

```text
                         User
                           │
                           ▼
                    OpsPilot AI UI
                           │
                           │ POST /ask
                           ▼
                     FastAPI API
                           │
                           ▼
                  Retrieve relevant
                   knowledge chunks
                           │
                           ▼
                       ChromaDB
                           │
                           ▼
                    Relevance Gate
                           │
                    ┌──────┴──────┐
                    │             │
                  YES             NO
                    │             │
                    ▼             ▼
              Azure OpenAI     Safe fallback
              Answer Generation    response
                    │
                    ▼
              Grounded Answer
                    │
                    ▼
               Source List
                    │
                    ▼
                       UI
```

## RAG Flow

```text
User Question
      │
      ▼
FastAPI /ask
      │
      ▼
Query ChromaDB
      │
      ▼
Retrieve Relevant Chunks
      │
      ▼
LLM Relevance Gate
      │
 ┌────┴────┐
 │         │
YES        NO
 │         │
 ▼         ▼
Azure      Safe
OpenAI     Fallback
 │
 ▼
Generate Grounded Answer
 │
 ▼
Return Answer + Sources
```

## Production Cloud Architecture

```text
                         GitHub
                           │
                        git push
                           │
                           ▼
                    GitHub Actions
                           │
             ┌─────────────┴─────────────┐
             │                           │
          Run Tests                  Docker Build
             │                           │
             └─────────────┬─────────────┘
                           │
                           ▼
                    Azure OIDC Login
                           │
                           ▼
                Azure Container Registry
                           │
                           │ Image tagged
                           │ with GITHUB_SHA
                           ▼
                  Azure Container Apps
                           │
                           ▼
                    OpsPilot AI API
                           │
              ┌────────────┴────────────┐
              │                         │
              ▼                         ▼
        Azure OpenAI              Log Analytics
              │                         │
              ▼                         ▼
       AI Responses                  KQL
```

## Azure Runtime Architecture

```text
                    Azure Container Apps
                             │
                             ▼
                    OpsPilot AI Container
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
           FastAPI        ChromaDB          UI
              │
              ▼
        Azure OpenAI
              │
              ▼
       Generated Response
              │
              ▼
       Log Analytics
              │
              ▼
             KQL
```

## Container Image Flow

```text
GitHub Actions
      │
      │ Azure OIDC
      ▼
Azure Container Registry
      │
      │ Container Registry
      │ Repository Writer
      ▼
opspilot-ai:<GITHUB_SHA>
      │
      │ Repository Reader
      ▼
Azure Container Apps
      │
      ▼
Running Container
```

---

# Azure Infrastructure

| Resource | Purpose |
|---|---|
| Resource Group | `opspilot-ai-rg` |
| Azure Container Registry | `opspilotaiacr01` |
| Container Apps Environment | `opspilot-ai-env` |
| Container App | `opspilot-ai` |
| Azure OpenAI | LLM inference and relevance evaluation |
| Log Analytics Workspace | Application and container observability |
| GitHub Entra App Registration | OIDC authentication for CI/CD |

### Azure Container Registry

The Docker image is stored in Azure Container Registry.

```text
Registry:
opspilotaiacr01-gagwerbedwhtdf8.azurecr.io

Repository:
opspilot-ai

Image tag:
<GITHUB_SHA>
```

Images are tagged using the Git commit SHA so every deployment can be traced to an exact source-code revision.

---

# CI/CD Pipeline

OpsPilot AI uses GitHub Actions for continuous integration and deployment.

```text
git push main
      │
      ▼
GitHub Actions
      │
      ▼
Install Dependencies
      │
      ▼
Build Knowledge Base
      │
      ▼
Start FastAPI
      │
      ▼
Run API E2E Tests
      │
      ▼
Build Docker Image
      │
      ▼
Azure OIDC Login
      │
      ▼
Login to ACR
      │
      ▼
Push Image to ACR
      │
      ▼
Deploy to Azure Container Apps
      │
      ▼
New Container Apps Revision
      │
      ▼
Production
```

## CI/CD Steps

The workflow performs the following:

1. Checks out the repository.
2. Sets up Python 3.11.
3. Authenticates to Azure using OpenID Connect.
4. Installs Python dependencies.
5. Builds the ChromaDB knowledge base.
6. Starts the FastAPI application.
7. Runs end-to-end API tests.
8. Builds the Docker image.
9. Authenticates to Azure Container Registry.
10. Tags the image using `GITHUB_SHA`.
11. Pushes the image to ACR.
12. Updates Azure Container Apps with the new image.

### Image Versioning

Every deployment uses the GitHub commit SHA as the Docker image tag.

```text
Git Commit
    │
    ▼
GITHUB_SHA
    │
    ▼
Docker Image
    │
    ▼
Azure Container Registry
    │
    ▼
Container Apps Revision
```

Example:

```text
opspilot-ai:<GITHUB_SHA>
```

This provides traceability between source code, container image, and production deployment.

---

# Security

## GitHub Actions Authentication

GitHub Actions authenticates to Azure using **OpenID Connect (OIDC)** rather than storing a long-lived Azure client secret.

The GitHub identity is configured using:

- Azure Entra application registration
- Federated identity credential
- GitHub repository
- `main` branch
- Azure tenant
- Azure subscription

This reduces the need for long-lived Azure credentials in GitHub.

## Azure OpenAI Secrets

Azure OpenAI credentials are stored as:

- GitHub Actions secrets for CI/CD
- Azure Container Apps secrets for runtime configuration

Secrets are not committed to the repository.

The local `.env` file is excluded using `.gitignore`.

---

# ACR Security

The Azure Container Registry uses **RBAC Registry + ABAC Repository Permissions**.

Repository-level permissions are used for container image access.

The GitHub deployment identity has permissions required to:

- authenticate to Azure
- push container images
- access the required registry resources
- deploy the Container App

The Container Apps environment identity has repository-level read access required to pull the application image.

### ACR Permission Model

```text
GitHub Actions Identity
          │
          │ Repository Writer
          ▼
Azure Container Registry
          │
          │ Repository Reader
          ▼
Container Apps Environment Identity
          │
          ▼
OpsPilot AI Container
```

ACR admin credentials are disabled.

The application therefore relies on Azure identity-based authentication rather than registry username/password authentication.

---

# Azure Container Apps

The application runs as an externally accessible HTTP Container App.

### Runtime Configuration

```text
CPU:
0.5

Memory:
1 GiB

Ingress:
External HTTP

Target Port:
8000
```

The container listens on:

```text
0.0.0.0:8000
```

This allows Azure Container Apps to route external traffic to the FastAPI application.

---

# Container Apps Revisions

Azure Container Apps creates a new revision when deployment-relevant configuration changes.

The deployment history therefore provides a record of application versions.

Example:

```text
Revision 00000002
        │
        ▼
Revision 00000003
        │
        ▼
Revision 00000004
```

The current production revision receives 100% of traffic.

This provides a foundation for:

- version tracking
- rollback
- controlled deployments
- revision-based troubleshooting

---

# Health Monitoring

OpsPilot AI exposes a health endpoint:

```http
GET /health
```

Example response:

```json
{
  "status": "Application is Running",
  "service": "OpsPilot AI"
}
```

Azure Container Apps health probes are used to determine container health.

The application includes:

- liveness monitoring
- readiness monitoring
- HTTP application health endpoint

The health endpoint is intentionally lightweight so that it can be used for container health verification without invoking the LLM.

---

# Observability

Application logs are available through Azure Container Apps and Azure Log Analytics.

The application logs important runtime events such as:

- API requests
- relevance decisions
- application errors
- exceptions
- container startup information

## View Recent Container Logs

```kusto
ContainerAppConsoleLogs_CL
| where TimeGenerated > ago(1h)
| order by TimeGenerated desc
```

## Search for Application Errors

```kusto
ContainerAppConsoleLogs_CL
| where TimeGenerated > ago(24h)
| where Log_s contains "ERROR"
    or Log_s contains "Exception"
    or Log_s contains "Traceback"
| order by TimeGenerated desc
```

## Revision-Specific Investigation

Logs can be filtered by revision/container group when investigating a particular deployment.

```kusto
ContainerAppConsoleLogs_CL
| where TimeGenerated > ago(24h)
| where ContainerGroupName_s contains "00000004"
| where Log_s contains "ERROR"
    or Log_s contains "Exception"
    or Log_s contains "Traceback"
| order by TimeGenerated desc
```

This makes it possible to distinguish historical failures from problems affecting the current production revision.

---

# Knowledge Base

OpsPilot AI uses a curated Markdown knowledge base covering common DevOps troubleshooting scenarios.

Current knowledge areas include:

```text
docs/
├── docker.md
├── kubernetes.md
├── linux.md
├── nginx.md
└── terraform.md
```

The knowledge base is ingested into ChromaDB during application/container build.

---

# Knowledge Ingestion

The ingestion process is handled by:

```text
scripts/ingest.py
```

The script:

1. Reads Markdown documents.
2. Splits content into meaningful sections.
3. Associates metadata with each chunk.
4. Generates vector representations.
5. Stores the resulting documents in ChromaDB.

The Docker image builds the knowledge base during image creation:

```text
Docker Build
     │
     ▼
scripts/ingest.py
     │
     ▼
ChromaDB
     │
     ▼
Application Runtime
```

The generated local ChromaDB directory is excluded from Git because it is a generated artifact.

---

# Relevance Gate

A key component of OpsPilot AI is the relevance gate.

The system does not automatically send every question to the answer-generation stage.

Instead:

```text
Question
   │
   ▼
Retrieve Knowledge
   │
   ▼
Evaluate Relevance
   │
 ┌─┴─┐
YES  NO
 │    │
 ▼    ▼
Answer  Fallback
```

If retrieved knowledge is sufficiently relevant:

```text
Relevance = YES
```

Azure OpenAI generates an answer using the retrieved context.

If the knowledge is insufficient:

```text
Relevance = NO
```

The system returns a safe fallback instead of generating an unsupported answer.

Example fallback:

```text
I don't have enough relevant information in the knowledge base to answer this question accurately.
```

This creates an explicit boundary around what the assistant is allowed to answer.

---

# API Endpoints

## Health Check

```http
GET /health
```

Used by:

- Azure Container Apps health monitoring
- operational checks
- deployment verification

## Ask Question

```http
POST /ask
```

Example request:

```json
{
  "question": "How do I troubleshoot a Kubernetes CrashLoopBackOff?"
}
```

The endpoint performs:

```text
Input Validation
      │
      ▼
Knowledge Retrieval
      │
      ▼
Relevance Evaluation
      │
      ▼
Answer Generation
      │
      ▼
Source Attribution
```

## Root Endpoint

```http
GET /
```

Serves the OpsPilot AI web interface.

---

# Example Queries

## Supported Question

```text
How do I troubleshoot a Kubernetes CrashLoopBackOff?
```

Expected behavior:

```text
Relevant knowledge found
        │
        ▼
Relevance: YES
        │
        ▼
Azure OpenAI
        │
        ▼
Grounded Kubernetes troubleshooting answer
        │
        ▼
Source: kubernetes.md
```

## Unsupported Question

```text
Where is my ingress?
```

Expected behavior:

```text
No relevant knowledge found
        │
        ▼
Relevance: NO
        │
        ▼
Safe fallback response
        │
        ▼
No unsupported answer generated
```

---

# Testing

The project includes end-to-end API tests:

```text
tests/api_e2e_test.py
```

The current test suite validates:

- Health endpoint
- Supported question
- Unsupported question
- Empty question validation

Current result:

```text
PASS: Health endpoint
PASS: Supported question
PASS: Unsupported question
PASS: Empty question validation

RESULT: 4/4 tests passed
```

The same test suite is executed as part of the GitHub Actions CI pipeline.

---

# Docker

OpsPilot AI is containerized using Docker.

The Docker image:

1. Uses Python 3.11.
2. Installs application dependencies.
3. Copies the FastAPI application.
4. Copies the knowledge base.
5. Copies the ingestion script.
6. Builds the ChromaDB knowledge base.
7. Exposes port 8000.
8. Starts Uvicorn.

Application startup command:

```text
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

# Docker Compose

Docker Compose is provided for local container orchestration.

The Compose configuration includes:

- Application container
- Port mapping
- Azure OpenAI environment variables
- Healthcheck
- Automatic restart policy

Example architecture:

```text
Docker Compose
      │
      ▼
OpsPilot AI Container
      │
      ├── FastAPI
      ├── ChromaDB
      └── UI
```

The container is configured with:

```text
restart: unless-stopped
```

This allows Docker to automatically restart the application after an unexpected container failure.

---

# Environment Variables

The application requires the following Azure OpenAI configuration:

```text
AZURE_OPENAI_ENDPOINT
AZURE_OPENAI_API_KEY
AZURE_OPENAI_DEPLOYMENT
```

For local development, these values can be provided through a `.env` file.

Example:

```env
AZURE_OPENAI_ENDPOINT=<your-azure-openai-endpoint>
AZURE_OPENAI_API_KEY=<your-api-key>
AZURE_OPENAI_DEPLOYMENT=<your-deployment-name>
```

The `.env` file must never be committed to Git.

It is excluded through `.gitignore`.

In Azure Container Apps:

```text
AZURE_OPENAI_ENDPOINT
        │
        ▼
Environment Variable

AZURE_OPENAI_API_KEY
        │
        ▼
Container Apps Secret

AZURE_OPENAI_DEPLOYMENT
        │
        ▼
Environment Variable
```

---

# Project Structure

```text
OpsPilot-AI/
│
├── app/
│   ├── main.py
│   ├── retriever.py
│   ├── relevance.py
│   └── generator.py
│
├── docs/
│   ├── docker.md
│   ├── kubernetes.md
│   ├── linux.md
│   ├── nginx.md
│   └── terraform.md
│
├── scripts/
│   └── ingest.py
│
├── tests/
│   └── api_e2e_test.py
│
├── ui/
│   └── index.html
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .dockerignore
├── .gitignore
└── README.md
```

---

# Local Development

## 1. Clone Repository

```bash
git clone https://github.com/bhavikk02/OpsPilot-AI.git
cd OpsPilot-AI
```

## 2. Create Virtual Environment

Windows PowerShell:

```powershell
python -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

## 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

## 4. Configure Environment Variables

Create a local `.env` file:

```env
AZURE_OPENAI_ENDPOINT=<your-azure-openai-endpoint>
AZURE_OPENAI_API_KEY=<your-api-key>
AZURE_OPENAI_DEPLOYMENT=<your-deployment-name>
```

## 5. Build Knowledge Base

```powershell
python scripts/ingest.py
```

## 6. Start Application

```powershell
uvicorn app.main:app --reload
```

The application runs locally on:

```text
http://127.0.0.1:8000
```

The web interface is available at the root URL.

---

# Local Docker Deployment

Build the Docker image:

```powershell
docker build -t opspilot-ai .
```

Run the container:

```powershell
docker run --env-file .env -p 8000:8000 opspilot-ai
```

Verify:

```text
http://localhost:8000/health
```

---

# Docker Compose Deployment

Start the application:

```powershell
docker compose up --build
```

Run in detached mode:

```powershell
docker compose up --build -d
```

Check running containers:

```powershell
docker ps
```

Check logs:

```powershell
docker logs opspilot-ai
```

---

# Production Deployment

Production deployment is automated through GitHub Actions.

A normal deployment is triggered by:

```text
git push origin main
```

The workflow then:

```text
GitHub
  │
  ▼
CI Tests
  │
  ▼
Docker Build
  │
  ▼
Azure Authentication via OIDC
  │
  ▼
ACR Push
  │
  ▼
Container Apps Update
  │
  ▼
New Revision
  │
  ▼
Production Traffic
```

No manual Docker image upload is required.

No long-lived Azure client secret is required for GitHub Actions authentication.

---

# Troubleshooting Approach

OpsPilot AI was designed with operational troubleshooting in mind.

A typical troubleshooting workflow is:

```text
1. Check application health
          │
          ▼
2. Check Container Apps revision
          │
          ▼
3. Check replica/container status
          │
          ▼
4. Inspect Log Stream
          │
          ▼
5. Query Log Analytics with KQL
          │
          ▼
6. Identify application or infrastructure failure
          │
          ▼
7. Deploy corrected revision
          │
          ▼
8. Verify health and application behavior
```

Examples of issues investigated during development included:

- Container image authorization failures
- Missing runtime environment variables
- Container startup crashes
- Incorrect frontend API endpoint
- Health probe configuration
- Container restart behavior
- Production application logs
- Revision-level troubleshooting

This project therefore demonstrates both application development and operational troubleshooting.

---

# DevOps Concepts Demonstrated

This project demonstrates practical experience with:

### Infrastructure and Cloud

- Azure Container Apps
- Azure Container Registry
- Azure OpenAI
- Azure Resource Groups
- Managed identities
- Azure Entra ID

### Containers

- Docker
- Docker Compose
- Docker image creation
- Container healthchecks
- Container restart policies
- Container image versioning

### CI/CD

- GitHub Actions
- Continuous integration
- Continuous deployment
- Automated testing
- Docker image build and push
- Commit-based image tagging
- Automated Azure deployment

### Security

- OpenID Connect
- Federated identity credentials
- Azure RBAC
- ACR Repository ABAC
- Managed identity
- Secret management
- No long-lived Azure credentials in GitHub Actions

### Observability

- Application logging
- Container logs
- Azure Log Analytics
- KQL
- Health endpoints
- Liveness monitoring
- Readiness monitoring
- Revision-specific troubleshooting

### AI / RAG

- Retrieval-Augmented Generation
- Vector search
- ChromaDB
- LLM relevance evaluation
- Grounded generation
- Source attribution
- Hallucination reduction
- Knowledge-base boundaries

---

# Engineering Decisions

## Why RAG?

A general-purpose LLM may generate technically plausible answers that are not supported by the organization's knowledge base.

RAG introduces a retrieval layer so answers can be grounded in curated information.

## Why a Relevance Gate?

Retrieval alone does not guarantee that the returned chunks are sufficient to answer the question.

The relevance gate provides an explicit decision point before answer generation.

## Why ChromaDB?

ChromaDB provides a lightweight vector database suitable for storing and retrieving embeddings for a focused knowledge base.

## Why Azure Container Apps?

Container Apps provides managed container hosting without requiring management of a Kubernetes cluster for this application.

It also provides:

- HTTPS ingress
- revisions
- scaling capabilities
- managed identity integration
- health monitoring
- Azure-native observability

## Why GitHub OIDC?

OIDC avoids storing long-lived Azure service principal secrets in GitHub Actions.

The workflow obtains temporary Azure authentication based on the federated identity configuration.

## Why Git SHA Image Tags?

Using the commit SHA as the Docker image tag makes deployments traceable.

A production revision can be mapped back to the exact Git commit that produced its container image.

---

# Future Improvements

Potential future improvements include:

- Streaming LLM responses
- More DevOps knowledge domains
- Authentication and authorization for users
- Role-based access control
- Conversation history
- Improved retrieval evaluation
- Hybrid keyword + vector search
- Automated knowledge-base updates
- Prometheus/Grafana metrics
- OpenTelemetry tracing
- Application performance monitoring
- Automated rollback based on health checks
- Infrastructure provisioning using Terraform
- Blue/green or canary deployment strategies
- Horizontal scaling based on workload
- Automated security scanning of container images

---

# Project Status

**Production deployment: Complete**

Current implementation includes:

- Functional FastAPI application
- Working RAG pipeline
- ChromaDB knowledge retrieval
- Azure OpenAI integration
- Relevance gate
- Grounded answer generation
- Safe unsupported-question handling
- Docker containerization
- Docker Compose
- Automated tests
- GitHub Actions CI/CD
- Azure OIDC authentication
- Azure Container Registry
- ACR Repository ABAC permissions
- Managed identity image pull
- Azure Container Apps deployment
- Container Apps revisions
- Health monitoring
- Azure Log Analytics
- KQL-based observability
- Production UI
- Automated deployment from GitHub to Azure

The production application has been validated with both supported and unsupported DevOps questions.

---

# Author

**Bhavik**

DevOps Engineer | Cloud | Automation | AI-assisted Infrastructure
