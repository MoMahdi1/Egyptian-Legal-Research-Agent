from langgraph.graph import StateGraph, END
from app.state import ResearchState
from app.agents.orchestrator import orchestrator_node
from app.agents.retriever_agent import retriever_agent
from app.agents.critic_agent import critic_node
from app.agents.writer_agent import writer_node

# Retriever Node

def retriever_node(state: ResearchState) -> ResearchState:
    
    queries = state.get("search_queries",[])
    
    if not queries:
        return {
            **state,
            "retrieval_results":[],
            "current_step":"critic"
        }
        
    all_results = []
    
    for query in queries:
        results = retriever_agent(query)
        all_results.append(results)
        
    print("\n========== RETRIEVAL RESULTS ==========\n")
    print(f"[retriever_node] Total Queries: {len(queries)}")
    
    
    for i , r in enumerate(all_results):
        
        print(
            f"[{i}]"
            f"source={r['source']} | "
            f"fallback={r['fallback_used']}"
        )
        
    return {
        **state,
        "retrieval_results": all_results,
        "current_step":"critic"
    }
    
# Build the graph

def build_graph():
    
    graph = StateGraph(ResearchState)
    
    # Nodes
    graph.add_node("orchestrator", orchestrator_node)
    graph.add_node("retriever", retriever_node)
    graph.add_node("critic", critic_node)
    graph.add_node("writer", writer_node)
    
    # Flows
    
    graph.set_entry_point("orchestrator")
    
    graph.add_edge("orchestrator", "retriever")
    graph.add_edge("retriever", "critic")
    graph.add_edge("critic", "writer")
    graph.add_edge("writer", END)
    
    
    return graph.compile()

# Graph instance

research_graph = build_graph()