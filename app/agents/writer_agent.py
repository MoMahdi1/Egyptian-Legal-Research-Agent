import os 
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from app.state import ResearchState
from dotenv import load_dotenv
from app.llms.provider import get_llm

load_dotenv()
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

llm = get_llm()


prompt = ChatPromptTemplate.from_template(
    """
    انت كاتب قانوني متخصص في القانون المصري المدني وكتابة الأبحاث القانونية.
    
    اكتب تقريرا قانونيا شاملا بناءً على السؤال التالى :
    
    السؤال :
    {question}
    السؤال المحسن: 
    {rewritten_query}
    
    المصادر:
    {results}
    
    محلاحظات المرجع القانوني :
    {critique}
    
    اكتب التقرير بهذا التنسيق بالضبط
    
    ## الملخص التنفيذي
    [ملخص مختصر فى 2-3 جمل]
    
    ## الاجابة القانونية
    [اجابة قانونية شاملة ومفصلة مدعمة بالمصادر القانونية]
    
    ## المواد القانونية ذات الصلة
    [اذكر ارقام المواد والنصوص المرتبطة]
    
    ## المصادر المستخدمة
    [documents / web]
    
    ## التحفظات 
    [اي تحفظات او توصيات للمراجعة النهائية]
    
    """
)

def format_results(retrieval_results: list) ->str:
    if not retrieval_results:
        return "لا توجد مصادر ."
    
    formatted = []
    
    # handel both dict or list
    if isinstance(retrieval_results, dict):
        retrieval_results = [retrieval_results]
        
        
    for r in retrieval_results:
        source = r.get("source","unknown")
        
        for item in r.get("results",[]):
            content = item.get("content","")
            
            formatted.append(
                f"[{source}] \n {content[:800]}\n"
            )
            
    return "\n".join(formatted)[:4000]


def writer_node(state: ResearchState) -> ResearchState:
    
    result_text = format_results(
        state.get("retrieval_results",[])
    )
        
        
    chain = prompt | llm
    result = chain.invoke({
        "question": state["question"],
        "rewritten_query": state.get("rewritten_query",""),
        "critique": state.get("critique"," لا توجد ملاحظات "),
        "results": result_text
    })
       
    print("\n========== WRITER OUTPUT ==========")
    print(result.content[:1000])
    
    return {
        **state,
        "final_report": result.content,
        "current_step": "final_report",
        
    }