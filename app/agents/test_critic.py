from app.agents.critic_agent import critic_node

fake_state = {
    "question": "هل يحق للمؤجر فسخ عقد الإيجار؟",

    "retrieval_results": [
        {
            "source": "documents",

            "results": [
                {
                    "content": "يجوز للمؤجر طلب فسخ عقد الإيجار عند عدم سداد الأجرة.",
                    "rerank_score": 1.22
                },

                {
                    "content": "تشترط المحكمة إنذار المستأجر قبل رفع الدعوى.",
                    "rerank_score": 0.87
                }
            ]
        }
    ]
}

result = critic_node(fake_state)

print("\n========== FINAL STATE ==========")
print(result["critique"])