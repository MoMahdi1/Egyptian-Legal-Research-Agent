import logging

from langchain_core.prompts import ChatPromptTemplate

from app.llms.provider import get_llm, invoke_llm
from app.state import ResearchState

logger = logging.getLogger(__name__)

# ===========================
# LLM
# ===========================

llm = get_llm()

# ===========================
# Prompt
# ===========================

prompt = ChatPromptTemplate.from_template("""
أنت مراجع قانوني متخصص في القانون المصري.

مهمتك تقييم جودة نتائج البحث فقط، ولا تُجب عن السؤال القانوني.

السؤال:
{question}

النتائج المسترجعة:
{results}

قيّم النتائج وفقًا للنقاط التالية:

1. مدى ارتباط النتائج بالسؤال.
2. مدى دقة المعلومات.
3. هل توجد نتائج غير مرتبطة؟
4. هل توجد معلومات ناقصة؟
5. مدى موثوقية المصادر.
6. هل تكفي هذه النتائج لكتابة تقرير قانوني قوي؟

أجب باللغة العربية فقط.
""")

# ===========================
# Helper
# ===========================

def format_results(retrieval_results: list) -> str:

    if not retrieval_results:
        return "لا توجد نتائج."

    formatted = []

    for retrieval in retrieval_results:

        source = retrieval.get("source", "unknown")

        for item in retrieval.get("results", []):

            content = item.get("content", "")[:500]

            rerank_score = item.get("rerank_score", "N/A")

            formatted.append(
                f"""
المصدر: {source}
درجة إعادة الترتيب: {rerank_score}

{content}
"""
            )

    return "\n\n".join(formatted)


# ===========================
# Critic Node
# ===========================

def critic_node(state: ResearchState) -> ResearchState:

    logger.info("========== ENTER CRITIC ==========")

    results_text = format_results(
        state.get("retrieval_results", [])
    )


    try:

        logger.info("Sending request to Critic LLM...")

        messages = prompt.format_messages(
            question = state["question"],
            results = results_text,
        )
        result = invoke_llm(llm,messages)

        logger.info("Critic LLM Response Received")

        logger.info(result.content)

        return {
            **state,
            "critique": result.content,
            "current_step": "writing"
        }

    except Exception as e:

        logger.exception("Critic Agent Failed")

        return {
            **state,
            "critique": "تعذر تقييم جودة النتائج بسبب خطأ أثناء تنفيذ مرحلة المراجعة.",
            "current_step": "writing"
        }
        
        
        