import logging

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate

from app.llms.provider import get_llm, invoke_llm
from app.state import ResearchState

load_dotenv()

logger = logging.getLogger(__name__)

llm = get_llm()

# ==========================================================
# Prompt
# ==========================================================
prompt = ChatPromptTemplate.from_template(
"""
أنت باحث قانوني متخصص في القانون المدني المصري.

مهمتك هي الإجابة عن السؤال اعتمادًا فقط على المصادر القانونية المسترجعة.

==========================
قواعد إلزامية
==========================

1. استخدم المعلومات الموجودة داخل المصادر فقط.
2. ممنوع استخدام أي معلومة من معرفتك العامة.
3. لا تخترع مواد قانونية.
4. لا تخترع أحكام محكمة النقض.
5. لا تستشهد إلا بالمواد الموجودة داخل المصادر.
6. إذا كانت المصادر لا تكفي للإجابة فاذكر ذلك بوضوح.
7. إذا كانت المصادر متعارضة فاذكر موضع التعارض.
8. تجاهل أي مصدر غير مرتبط بالسؤال.
9. لا تكرر نفس المعلومة أكثر من مرة.
10. اجعل الإجابة طبيعية وكأنها صادرة من مستشار قانوني.

==========================
السؤال
==========================

{question}

==========================
السؤال بعد إعادة الصياغة
==========================

{rewritten_query}

==========================
المصادر المسترجعة
==========================

{results}

==========================
تقييم جودة المصادر
==========================

{critique}

==========================
المطلوب
==========================

قم أولاً بتحليل المصادر.

بعد ذلك أجب على السؤال بهذا التنسيق فقط:

## الإجابة المختصرة

- اكتب إجابة مباشرة من 3 إلى 5 أسطر.
- إذا كان السؤال يحتاج نعم أو لا فابدأ بها.
- لا تذكر أسماء الوثائق أو الصفحات.

---

## الإجابة القانونية

اشرح الإجابة بالتفصيل اعتمادًا فقط على النصوص القانونية الموجودة بالمصادر.

- اذكر أرقام المواد القانونية داخل الشرح عند الحاجة.
- اربط بين المواد إذا كان ذلك يساعد على الفهم.
- إذا لم توجد إجابة مباشرة داخل المصادر فاذكر:
"المعلومات القانونية المتاحة لا تكفي للإجابة بدقة."
- لا تضف أي معلومات من خارج المصادر.
- لا تذكر قسمًا للمصادر.
- لا تذكر مستوى الثقة.
- لا تذكر التحفظات.
- لا تذكر أي عناوين أخرى غير المطلوبة.
"""
)

# ==========================================================
# Helpers
# ==========================================================

def format_results(retrieval_results: list) -> str:

    if not retrieval_results:
        return "لا توجد مصادر."

    if isinstance(retrieval_results, dict):
        retrieval_results = [retrieval_results]

    formatted = []

    counter = 1

    for retrieval in retrieval_results:

        source = retrieval.get("source", "unknown")

        for item in retrieval.get("results", []):

            content = item.get("content", "")
            metadata = item.get("metadata", {})

            formatted.append(
f"""
======================================================
Document {counter}

Source:
{source}

Source File:
{metadata.get("source", "Unknown")}

Page:
{metadata.get("page", "N/A")}

Content:
{content[:1000]}

======================================================
"""
            )

            counter += 1

    return "\n".join(formatted)

# ==========================================================
# Writer Node
# ==========================================================

def writer_node(state: ResearchState) -> ResearchState:

    logger.info("========== ENTER WRITER ==========")

    results_text = format_results(
        state.get("retrieval_results", [])
    )

    if results_text.strip() == "لا توجد مصادر.":

        logger.warning("No retrieved documents.")

        return {
            **state,
            "final_report": "لم يتم العثور على مصادر قانونية كافية للإجابة على السؤال.",
            "current_step": "final_report",
        }

    

    logger.info("Sending request to Writer LLM...")

    messages = prompt.format_messages(
        question=state["question"],
        rewritten_query=state.get("rewritten_query", ""),
        results=results_text,
        critique=state.get(
          "critique",
          "لا توجد ملاحظات."
    ),
)

    result = invoke_llm(llm, messages)

    logger.info("Writer LLM Response Received")

    logger.info("=" * 60)
    logger.info("WRITER OUTPUT")
    logger.info(result.content)
    logger.info("=" * 60)

    return {
        **state,
        "final_report": result.content,
        "current_step": "final_report",
    }