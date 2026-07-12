from typing import TypedDict, List, Optional, Dict, Any


class ResearchState(TypedDict):
    question: str

    # Orchestrator
    rewritten_query: Optional[str]
    search_queries: List[str]

    # Retrieval
    retrieval_results: List[Dict[str, Any]]

    # Critic
    critique: Optional[str]

    # Writer
    final_report: Optional[str]

    # Status
    current_step: str