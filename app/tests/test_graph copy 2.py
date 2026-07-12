from app.graph import research_graph

initial_state = {
    "question": "هل يحق للمؤجر فسخ عقد الإيجار عند عدم سداد الأجرة؟",

    "rewritten_query": None,
    "search_queries": [],

    "retrieval_results": [],

    "critique": None,
    "final_report": None,

    "current_step": "start",
}

# تشغيل الـ graph
result = research_graph.invoke(initial_state)

print("\n========== FINAL REPORT ==========\n")

print(result["final_report"])