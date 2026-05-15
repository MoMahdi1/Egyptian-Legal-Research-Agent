import os
from tavily import TavilyClient


clinet = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def web_search(query:str , max_results : int = 5):
    try:
        results = clinet.search(
            query=query,
            max_results=max_results,
            search_depth="advanced"
        )
        
        formatted_results = []
        
        for i in results.get("results",[]):
            score = i.get("score" , 0)
            
            if score <0.5:
                continue
            
            formatted_results.append({
                "title": i.get("title" , "No Title"),
                "url": i.get("url" , ""),
                "content" : i.get("content",""),
                "score": score
            })
            
            
        return formatted_results
        
        
    except Exception as e:
        return [{
            "error": str(e)
        }]