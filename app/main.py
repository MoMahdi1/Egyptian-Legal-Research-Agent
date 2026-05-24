import os
import asyncio 
import logging
from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.graph import research_graph

load_dotenv()
# Logging Configuration
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

# APP

app = FastAPI(
    title="المستشار القانونى المصري - Egyptian Legal Advisor",
    description="نظام ذكي متعدد الوكلاء لمساعدتك في الأبحاث القانونية المصرية",
    version="1.0.0",
    
    
)


# CORS Middleware 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Schemas

class ResearchRequest(BaseModel):
    question: str
    
    
class ResearchResponse(BaseModel):
    original_question: str
    rewritten_query: str
    report: str
    critique: str
    queries_used: List[str]
    sources: List[str]
    
    
# Root

@app.get("/")
def root():
    return{
        "service":" Egyptian Legal Research Agent",
        "status":"running",
        "docs":"/docs"
    }
    
# Research Endpoint

@app.post("/research", response_model=ResearchResponse)
async def research(request: ResearchRequest):
    try:
        
        logger.info(f"Received research request: {request.question}")
        # Initialize state
        initial_state = {
            "question": request.question,
            "rewritten_query": None,
            "search_queries": [],
            "retrieval_results": [],
            "critique": None,
            "final_report": None,
            "current_step": "orchestrating",
        }
        
        # Run the research graph
        result = await asyncio.to_thread(
            research_graph.invoke,
            initial_state
        )
        
        logger.info("Research completed successfully.")
        
        sources = list({
            r.get("source","unknown") 
            for r in result.get("retrieval_results",[])
        })
        
        return ResearchResponse(
            original_question=result.get("question") or "",
            rewritten_query=result.get("rewritten_query") or "",
            report=result.get("final_report") or "",
            critique=result.get("critique") or "",
            queries_used=result.get("search_queries") or [],
            sources=sources,
        )
        
    except Exception as e:
        
        logger.exception("Research pipeline failed.")
        
        raise HTTPException(
            status_code=500,
            detail=str(e)
                        )

# Health

@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "Egyptian Legal Research Agent",
            }