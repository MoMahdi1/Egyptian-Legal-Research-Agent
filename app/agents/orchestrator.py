import os
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from app.state import ResearchState
from dotenv import load_dotenv
from app.llms.provider import get_llm
load_dotenv()

## LLM
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

llm = get_llm()

## Query Rewriting Prompt
rewrite_prompt = ChatPromptTemplate.from_template(
    """
   أنت خبير قانوني متخصص في القانون المصري وإعادة صياغة استعلامات البحث القانونية.

المهمة:
إعادة صياغة السؤال ليصبح مناسبًا لمحركات البحث القانونية وأنظمة RAG.

قواعد مهمة:
- حافظ على المعنى الأصلي بالكامل
- استخدم مصطلحات قانونية دقيقة
- حسّن الكلمات المفتاحية
- اجعل السؤال واضحًا ومحدداً
- إذا كان السؤال متعلقًا بالقانون أضف سياق "في القانون المصري"
- لا تشرح
- لا تضف إجابات
- أرجع السؤال المحسن فقط

السؤال:
{query}

السؤال المحسن:
"""
)

## Rewrite Function

def rewrite_query(query:str) -> str:
    chain = rewrite_prompt | llm
    
    response = chain.invoke({
        "query":query
    })
    
    return response.content.strip()


## Orchestrator Node

def orchestrator_node(state: ResearchState) -> ResearchState:
    
    original_question = state["question"]
    
    # Rewrite the original query
    improved_query = rewrite_query(original_question)
    print("=== REWRITE TEST ===")
    print(improved_query)
    # Generate multiple search queries
    generation_prompt = f"""
    انت باحث قانونى متخصص فى القانون المصرى .
    
    المطلوب:
    توليد استعلامات بحث احترافيه ومتنوعة تساعد نظام 
    RAG
    على استرجاع افضل الوثائق القانونية .
    
    السوؤال:
    {improved_query}
    
    التعليمات :
    - انشئ 3 استعلامات مختلفة
    - كل استعلام يركز على زاوية مختلفة
    - استخدم مصطلحات قانونية دقيقة
    - تجنب التكرار
    - اجعل الاستعلام مناسب للبحث الدلالى Semantic Search
    - اعد النتيجة فقط بصيغة JSON Array
    
    مثال :
    [
    "شروط فسخ عقد الإيجار في القانون المصري",
    "أحكام محكمة النقض المصرية بشأن فسخ عقود الإيجار",
    "الفرق بين الفسخ والبطلان في القانون المدني المصري"
    ]
    
    """
    
    response = llm.invoke(generation_prompt)
    
    ## Parser Response
    
    try:
        
        cleaned = response.content.strip()
        
        cleaned = cleaned.replace("```json","")
        cleaned = cleaned.replace("```","")
        
        queries = json.loads(cleaned)
        
        if not isinstance(queries , list):
            raise ValueError("Response is not a list")
        
        # remove duplicates 
        queries = list(dict.fromkeys(
            q.strip() for q in queries if q.strip()
            ))
        
        if len(queries) < 3:
            queries.append(improved_query)
    
    except Exception as e:
        print(f"[ERROR] Failed to parse queries: {e}")

        queries = [improved_query]
        
    ## Logs
    
    print("\n========== ORCHESTRATOR =========")
    print(f"[original] {original_question}")
    print(f"[rewritten] {improved_query}")
    
    for i , q in enumerate(queries,1):
        print(f"[query {i}] {q}")
        
        
    # Return Updated State
       
    return {
        **state,
        "rewritten_query": improved_query,
        "search_queries": queries,
        "current_step": "retrieving",
    }   
    