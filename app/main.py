import asyncio
import logging
from typing import List

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.graph import research_graph

load_dotenv()

# ==========================================================
# Logging
# ==========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

# ==========================================================
# FastAPI App
# ==========================================================

app = FastAPI(
    title="Egyptian Legal Research Agent",
    description="Multi-Agent AI System for Egyptian Legal Research",
    version="1.0.0",
)

# ==========================================================
# CORS
# ==========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================================
# Request / Response Models
# ==========================================================

class ResearchRequest(BaseModel):
    question: str


class ResearchResponse(BaseModel):
    original_question: str
    rewritten_query: str
    report: str
    critique: str
    queries_used: List[str]
    sources: List[str]


# ==========================================================
# Root Endpoint
# ==========================================================

@app.get("/")
def root():
    return {
        "service": "Egyptian Legal Research Agent",
        "status": "running",
        "docs": "/docs"
    }


# ==========================================================
# Health Check
# ==========================================================

@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "Egyptian Legal Research Agent"
    }


# ==========================================================
# Research Endpoint
# ==========================================================

@app.post("/research", response_model=ResearchResponse)
async def research(request: ResearchRequest):

    # -------------------------
    # Validate Input
    # -------------------------

    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    logger.info(f"Received Question: {question}")

    # -------------------------
    # Initial Graph State
    # -------------------------

    initial_state = {
        "question": question,
        "rewritten_query": None,
        "search_queries": [],
        "retrieval_results": [],
        "critique": None,
        "final_report": None,
        "current_step": "orchestrating",
    }

    try:

        # -------------------------
        # Run LangGraph
        # -------------------------

        result = await asyncio.to_thread(
            research_graph.invoke,
            initial_state
        )

        logger.info("Research completed successfully.")

        # -------------------------
        # Extract Sources
        # -------------------------

        sources = list({
            item.get("source", "unknown")
            for item in result.get("retrieval_results", [])
        })

        # -------------------------
        # API Response
        # -------------------------

        return ResearchResponse(
            original_question=result.get("question", ""),
            rewritten_query=result.get("rewritten_query", ""),
            report=result.get("final_report", ""),
            critique=result.get("critique", ""),
            queries_used=result.get("search_queries", []),
            sources=sources,
        )

    except HTTPException:
        raise

    except Exception as e:

        logger.exception("Research pipeline failed.")

        raise HTTPException(
            status_code=500,
            detail=f"Internal Server Error: {str(e)}"
        )