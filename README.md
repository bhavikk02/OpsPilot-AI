# OpsPilot AI 🚀

AI-powered DevOps assistant that uses Retrieval-Augmented Generation (RAG) to answer infrastructure and DevOps troubleshooting questions from a curated internal knowledge base.

## Overview

OpsPilot AI is an internal AI assistant designed for DevOps teams.

Instead of relying only on an LLM's general knowledge, OpsPilot first retrieves relevant information from a curated DevOps knowledge base and checks whether the retrieved information is sufficient to answer the question.

If the knowledge is relevant, Azure OpenAI generates the final answer.

If the knowledge base does not contain enough relevant information, OpsPilot refuses to generate an unsupported answer.

This helps reduce hallucinations and keeps responses grounded in the available knowledge.

---

## Architecture

```text
                         Docker Compose
                              │
                              ▼
                         Docker Build
                              │
                 ┌────────────┴────────────┐
                 │                         │
              docs/                 scripts/ingest.py
                 │                         │
                 │                    Processes docs
                 │                         │
                 └────────────┬────────────┘
                              ▼
                         ChromaDB
                    Knowledge Base
                              │
                              ▼
                         FastAPI API
                              │
                            /ask
                              │
                    ┌─────────┴─────────┐
                    ▼                   ▼
              ChromaDB            Azure OpenAI
              Retrieval           Relevance Check
                    │                   │
                    └─────────┬─────────┘
                              ▼
                       Answer Generation
                              │
                              ▼
                            UI