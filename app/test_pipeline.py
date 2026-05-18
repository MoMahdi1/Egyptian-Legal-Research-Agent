from app.agents.orchestrator import orchestrator_node
from app.agents.retriever_agent import retriever_agent

# Initial State
state = {
    "question": "هل يحق للمؤجر فسخ عقد الإيجار عند عدم سداد الأجرة؟",
    "rewritten_query": None,
    "search_queries": [],
    "web_results": [],
    "doc_results": [],
    "critique": None,
    "final_report": None,
    "current_step": "orchestrating",
}

# =========================
# STEP 1 → ORCHESTRATOR
# =========================

state = orchestrator_node(state)

print("\n========== AFTER ORCHESTRATOR ==========\n")

print("Rewritten Query:")
print(state["rewritten_query"])

print("\nGenerated Queries:")

for q in state["search_queries"]:
    print("-", q)

# =========================
# STEP 2 → RETRIEVAL
# =========================

all_results = []

for query in state["search_queries"]:

    print(f"\n\n========== RETRIEVING ==========")
    print(f"Query: {query}")

    result = retriever_agent(query)

    all_results.append(result)

# =========================
# FINAL
# =========================

print("\n\n========== FINAL RESULTS ==========\n")

for i, result in enumerate(all_results, 1):

    print(f"\n--- Retrieval {i} ---")

    print("Source:", result["source"])
    print("Fallback:", result["fallback_used"])

    print("\nTop Results:\n")

    for j, doc in enumerate(result["results"], 1):

        print(f"Result {j}")

        if "rerank_score" in doc:
            print("Rerank Score:", doc["rerank_score"])

        if "score" in doc:
            print("Vector Score:", doc["score"])

        print(doc["content"][:300])
        print("\n====================\n")