# Learn Generative AI

A hands-on learning repository covering **Generative AI** concepts and **AI-powered microservices** architecture. This repository contains practical implementations, experiments, and mini-projects built while exploring closed-source hosted models (OpenAI, Gemini) and production-grade microservices patterns.

---

## Repository Structure

```
learn-generative-ai/
├── 00_closed_source_hosted_models/   # OpenAI & Gemini API explorations
│   ├── 00_learning_openai/           # OpenAI API features
│   ├── 01_learning_gemini/           # Google Gemini API features
│   └── 02_voice_agent_mvp/           # Real-time voice agent (WebSockets + uv)
│
├── 01_microservices_all_in_one_platform/  # Infrastructure & platform patterns
│   ├── 00_python_poetry/             # Python dependency management with Poetry
│   ├── 01_docker/                    # Docker dev containers, Compose & containerization
│   ├── 02_event_driven/              # Event-driven architecture with Kafka
│   └── 03_oauth2_auth/               # OAuth 2.0 implementation & endpoint authorization
│
└── xx_projects/                      # End-to-end applied AI projects
    ├── 01-scouts-ai/
    ├── 02-rag-mistral-ai/
    └── 03-rag-openai/
```

---

## Modules

### 00 — Closed-Source Hosted Models

Practical exploration of leading proprietary LLM APIs.

#### `00_learning_openai`
Hands-on work with the OpenAI API covering:
- **Knowledge Retrieval** — file-based retrieval with the Assistants API
- **Function Calling** — structured tool use and external API integration
- **Code Interpreter** — dynamic code execution within assistant threads

#### `01_learning_gemini`
Experiments with the Google Gemini API including:
- **Querying Gemini** — prompt design, multimodal inputs, and response handling
- **Socket Programming with Gemini** — real-time streaming via WebSocket connections

#### `02_voice_agent_mvp`
A minimal viable voice agent built with:
- **FastAPI + Uvicorn** — lightweight async HTTP/WebSocket server
- **WebSockets** — real-time bidirectional audio streaming
- **python-dotenv** — environment-based configuration
- **uv** — fast Python package and project manager

---

### 01 — Microservices All-in-One Platform

A progressive series of infrastructure and platform engineering topics, building towards a production-ready microservices environment.

#### `00_python_poetry`
Python project management with **Poetry** — dependency resolution, virtual environments, and packaging best practices.

#### `01_docker`
Container-based development patterns:
- **Dev Containers** — reproducible development environments with VS Code
- **Compose with Databases** — multi-service setups with PostgreSQL/Redis
- **Containerization** — Dockerfile best practices and image optimization

#### `02_event_driven`
Event-Driven Architecture (EDA) using **Apache Kafka**:
- **EDA Challenge** — practical problem-solving with asynchronous messaging
- **Kafka Single-Node Compose** — local Kafka cluster via Docker Compose
- **Kafka Messaging** — producers, consumers, and topic management
- **Protobuf** — schema definition and binary serialization
- **Schema Registry** — centralized schema management and Avro/Protobuf integration

#### `03_oauth2_auth`
OAuth 2.0 implementation from the ground up:
- **Generate Access Tokens** — client credentials and token issuance
- **Implement Auth** — authorization server setup and grant flows
- **Authorize Endpoints** — protected route enforcement and token validation

---

### xx — Projects

Applied, end-to-end AI projects combining models with real workloads.

| Project | Description |
|---|---|
| `01-scouts-ai` | AI assistant for scouts / domain-specific Q&A |
| `02-rag-mistral-ai` | Retrieval-Augmented Generation pipeline using Mistral AI |
| `03-rag-openai` | RAG pipeline powered by OpenAI embeddings and GPT models |

---

## Tech Stack

| Area | Technologies |
|---|---|
| LLM APIs | OpenAI API, Google Gemini API |
| Backend | Python, FastAPI, Uvicorn |
| Real-time | WebSockets |
| Package Management | uv, Poetry |
| Containerization | Docker, Docker Compose |
| Messaging | Apache Kafka, Protobuf, Schema Registry |
| Auth | OAuth 2.0 |
| Config | python-dotenv |

---

## Getting Started

Each module is self-contained. Navigate into any subdirectory and follow the instructions specific to that project.

**For `uv`-based projects** (e.g., `02_voice_agent_mvp`):
```bash
cd 00_closed_source_hosted_models/02_voice_agent_mvp
uv sync
uv run app
```

**For Poetry-based projects**:
```bash
cd 01_microservices_all_in_one_platform/00_python_poetry/00_poetry_projects
poetry install
poetry run <script>
```

**For Docker-based projects**:
```bash
cd 01_microservices_all_in_one_platform/01_docker/<sub-module>
docker compose up --build
```

> **Note:** Each project may require its own `.env` file. Copy the relevant `.env.example` (if provided) and fill in your API keys before running.

---

## Author

**Harry5174** — [harisjaved010@gmail.com](mailto:harisjaved010@gmail.com)

---

*This repository is a living learning resource and is actively updated as new topics are explored.*
