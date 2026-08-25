import logging
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field, field_validator

from app.retriever import retrieve_chunks
from app.relevance import check_relevance
from app.generator import generate_answer


# ============================================================
# Logging configuration
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


# ============================================================
# 1. FastAPI application
# ============================================================

app = FastAPI(
    title="OpsPilot AI",
    description="Internal AI Assistant for DevOps Teams",
    version="1.0.0"
)
UI_PATH = Path(__file__).resolve().parent.parent / "ui"

@app.get("/", include_in_schema=False)
def serve_ui():
    return FileResponse(UI_PATH / "index.html")


# ============================================================
# CORS configuration
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# 2. Request model
# ============================================================

class Question(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        description="DevOps question for OpsPilot"
    )

    @field_validator("question")
    @classmethod
    def validate_question(cls, value: str) -> str:

        value = value.strip()

        if not value:
            raise ValueError("Question cannot be empty.")

        return value


# ============================================================
# 3. Home endpoint
# ============================================================

@app.get("/")
def home():
    return {
        "message": "Welcome to OpsPilot AI 🚀"
    }


# ============================================================
# 4. Health endpoint
# ============================================================

@app.get("/health")
def health():
    return {
        "status": "Application is Running",
        "service": "OpsPilot AI"
    }


# ============================================================
# 5. Ask endpoint
# ============================================================

@app.post("/ask")
def ask_question(data: Question):

    question = data.question

    logger.info(
        "Received question: %s",
        question
    )

    try:

        # ----------------------------------------------------
        # Step 1: Retrieve knowledge
        # ----------------------------------------------------

        logger.info(
            "Retrieving knowledge from ChromaDB"
        )

        retrieved = retrieve_chunks(
            question=question,
            n_results=3
        )

        metadatas = retrieved["metadatas"]
        context = retrieved["context"]

        logger.info(
            "Retrieved %d chunks",
            len(retrieved["documents"])
        )

        # ----------------------------------------------------
        # Step 2: Relevance check
        # ----------------------------------------------------

        logger.info(
            "Running relevance check"
        )

        decision = check_relevance(
            question=question,
            context=context
        )

        logger.info(
            "Relevance decision: %s",
            decision
        )

        # ----------------------------------------------------
        # Step 3: Generate answer
        # ----------------------------------------------------

        if decision == "YES":

            logger.info(
                "Generating answer"
            )

            answer = generate_answer(
                question=question,
                context=context
            )

        else:

            logger.info(
                "Knowledge base is insufficient"
            )

            answer = (
                "I don't have enough relevant information "
                "in the knowledge base to answer this "
                "question accurately."
            )

        # ----------------------------------------------------
        # Step 4: Build source list
        # ----------------------------------------------------

        sources = []

        if decision == "YES":
            for metadata in metadatas:

                source = metadata.get(
                    "source",
                    "Unknown"
                )

                if source not in sources:
                    sources.append(source)

        # ----------------------------------------------------
        # Step 5: Return response
        # ----------------------------------------------------

        return {
            "your_question": question,
            "relevant": decision == "YES",
            "relevance_decision": decision,
            "answer": answer,
            "sources": sources
        }

    except Exception:

        logger.exception(
            "Error while processing question"
        )

        raise HTTPException(
            status_code=500,
            detail="OpsPilot could not process the request."
        )