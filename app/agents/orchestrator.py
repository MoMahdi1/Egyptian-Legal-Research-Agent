import json
import logging

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate

from app.llms.provider import get_llm
from app.state import ResearchState

load_dotenv()

logger = logging.getLogger(__name__)

llm = get_llm()

orchestrator_prompt = ChatPromptTemplate.from_template("""
أنت محرك إعادة صياغة للأسئلة القانونية المصرية.

هدفك:
تحويل سؤال المستخدم إلى نسخة مناسبة للبحث داخل قاعدة بيانات قانونية (RAG)،
ثم إنشاء 3 استعلامات بحث قريبة جداً من السؤال.

مهم جداً:

- لا تغير موضوع السؤال.
- لا تغير نوع العقد أو الجريمة أو القانون.
- لا تستخدم كلمات ليست موجودة فى السؤال إلا لو كانت مرادفات قانونية مباشرة.
- لا تحول البيع إلى إيجار.
- لا تحول المدني إلى تجاري.
- لا تضيف مواضيع جديدة.
- لا تستخدم كلمات عامة.
- الاستعلامات الثلاثة يجب أن تكون قريبة جداً من السؤال الأصلى.

أرجع JSON فقط.

{{
    "rewritten_query":"...",
    "queries":[
        "...",
        "...",
        "..."
    ]
}}

السؤال:

{query}
""")


def invoke_orchestrator(question: str):

    chain = orchestrator_prompt | llm

    response = chain.invoke(
        {
            "query": question
        }
    )

    cleaned = (
        response.content
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    return json.loads(cleaned)


def orchestrator_node(state: ResearchState):

    original_question = state["question"]

    try:

        data = invoke_orchestrator(original_question)

        improved_query = data.get(
            "rewritten_query",
            original_question
        )

        queries = data.get(
            "queries",
            []
        )

        if not isinstance(queries, list):
            raise Exception()

        queries = [
            q.strip()
            for q in queries
            if isinstance(q, str) and q.strip()
        ]

        queries = list(dict.fromkeys(queries))

        if improved_query not in queries:
            queries.insert(0, improved_query)

        queries = queries[:3]

        while len(queries) < 3:
            queries.append(improved_query)

    except Exception as e:

        logger.exception("Orchestrator Parsing Error")

        improved_query = original_question

        queries = [
            original_question,
            original_question,
            original_question
        ]

    logger.info("=" * 60)
    logger.info("ORCHESTRATOR")

    logger.info(f"Original : {original_question}")
    logger.info(f"Rewrite  : {improved_query}")

    for i, q in enumerate(queries, 1):
        logger.info(f"Query {i}: {q}")

    logger.info("=" * 60)

    return {
        **state,
        "rewritten_query": improved_query,
        "search_queries": queries,
        "current_step": "retrieving"
    }