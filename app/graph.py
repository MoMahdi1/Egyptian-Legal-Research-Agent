import logging

from langgraph.graph import StateGraph, END

from app.state import ResearchState
from app.agents.orchestrator import orchestrator_node
from app.agents.retriever_agent import retriever_agent
from app.agents.critic_agent import critic_node
from app.agents.writer_agent import writer_node

logger = logging.getLogger(__name__)


# ===========================
# Retriever Node
# ===========================

def retriever_node(state: ResearchState) -> ResearchState:

    queries = state.get("search_queries", [])

    if not queries:

        logger.warning("No search queries generated.")

        return {
            **state,
            "retrieval_results": [],
            "current_step": "critic"
        }

    logger.info("========== RETRIEVER ==========")
    logger.info(f"Queries Count: {len(queries)}")

    for i, query in enumerate(queries, start=1):
        logger.info(f"Query {i}: {query}")

    # Run ONE retrieval for ALL queries
    retrieval_result = retriever_agent(queries)

    logger.info(
        f"""
Retrieval Finished
Source   : {retrieval_result.get("source")}
Fallback : {retrieval_result.get("fallback_used")}
Results  : {len(retrieval_result.get("results", []))}
"""
    )

    return {
        **state,
        "retrieval_results": [retrieval_result],
        "current_step": "critic"
    }


# ===========================
# Build Graph
# ===========================

def build_graph():

    graph = StateGraph(ResearchState)

    # Nodes
    graph.add_node("orchestrator", orchestrator_node)
    graph.add_node("retriever", retriever_node)
    graph.add_node("critic", critic_node)
    graph.add_node("writer", writer_node)

    # Entry Point
    graph.set_entry_point("orchestrator")

    # Flow
    graph.add_edge("orchestrator", "retriever")
    graph.add_edge("retriever", "critic")
    graph.add_edge("critic", "writer")
    graph.add_edge("writer", END)

    return graph.compile()


# ===========================
# Graph Instance
# ===========================

research_graph = build_graph()