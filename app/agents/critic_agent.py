import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from app.state import ResearchState

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(
    model = "gemini-2.5-flash",
    google_api_key = GOOGLE_API_KEY ,
    temperature = 0
)

## Prompt 

prompt = ChatPromptTemplate.from_template(
    """
   أنت خبير قانوني متخصص في القانون المصري المدني وتقييم جودة الأبحاث القانونية.
   السؤال :
   {question}
   
   النتائج المسترجعة من البحث القانوني:
   {results}
   
   المطلوب :
    قم بتقييم جودة النتائج المسترجعة بناءً على مدى صلتها ودقتها وشموليتها من حيث بعض النقاط :
    1. هل النتائج المسترجعة مرتبطة بالسؤال ؟
    2. هل توجد معلومات ضعيفة او غير مرتبطة ؟
    3. هل توجد مععلومات ناقصة ؟
    4. ما مدى موثوقية النتائج ؟
    
    
    أجب باللعة العربية فقط .
    
    
   
   """
)

# Helpers 
def format_results(retrieval_results: list) ->str:
    if not retrieval_results:
        return "لا توجد نتائج"
    
    formatted = []
    for retrieval in retrieval_results:
        
        source = retrieval.get("source","unknown")
        
        for item in retrieval.get("results",[]):
            content = item.get("content","")
            
            rerank_score = item.get("rerank_score","N/A")
            formatted.append(
                f"""
                [Source: {source}]
                [RERANK SCORE: {rerank_score}]
                
                {content}
                """
            )
                
    return "\n".join(formatted)[:4000]
        
## Critic Node

def critic_node(state: ResearchState) -> ResearchState:
    
    results_text = format_results(
        state.get("retrieval_results",[])
        
    )
    
    chain = prompt | llm
    result = chain.invoke({
        "question": state["question"],
        "results": results_text
    })
    
    print("\n********** CRITIC **********")
    print(result.content)
    
    return {
        **state,
        "critique": result.content,
        "current_step": "writing"
    }
            
            


