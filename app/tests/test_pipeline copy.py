from app.agents.orchestrator import orchestrator_node
from app.agents.retriever_agent import retriever_agent
from app.agents.critic_agent import critic_node
from app.agents.writer_agent import writer_node


# =========================
# INITIAL STATE
# =========================

state = {
    "question": "هل يحق للمؤجر فسخ عقد الإيجار عند عدم سداد الأجرة؟",
    "rewritten_query": None,
    "search_queries": [],
    "retrieval_results": [],
    "critique": None,
    "final_report": None,
    "current_step": "orchestrating",
}

# =========================
# STEP 1 → ORCHESTRATOR
# =========================

state = orchestrator_node(state)

print("\n========== AFTER ORCHESTRATOR ==========\n")
print("Rewritten Query:", state["rewritten_query"])

print("\nGenerated Queries:")
for q in state["search_queries"]:
    print("-", q)


# =========================
# STEP 2 → RETRIEVAL + RERANK
# =========================

all_results = []

for query in state["search_queries"]:

    print(f"\n========== RETRIEVING ==========")
    print("Query:", query)

    result = retriever_agent(query)
    all_results.append(result)

# مهم جدًا: نحط النتائج في state
state["retrieval_results"] = all_results

# =========================
# STEP 3 → CRITIC
# =========================

print("\n========== CRITIC PHASE ==========\n")

state = critic_node(state)

print(state["critique"])


# =========================
# STEP 4 → WRITER
# =========================

print("\n========== WRITER PHASE ==========\n")

state = writer_node(state)

print(state["final_report"])


# =========================
# DONE
# =========================

print("\n========== PIPELINE DONE ==========")