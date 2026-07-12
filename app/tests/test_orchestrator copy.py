from app.agents.orchestrator import orchestrator_node

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

result = orchestrator_node(state)

print("\n========== FINAL STATE ==========\n")

print(result)