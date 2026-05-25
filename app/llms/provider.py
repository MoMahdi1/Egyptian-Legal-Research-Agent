import os 
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq

load_dotenv()

def get_llm():
    provider = os.getenv("LLM_PROVIDER","openai")
    
    if provider == "openai":
        print("Using OpenAI as LLM provider")
        return ChatOpenAI(
            model="gpt-4o-mini",
            api_key=os.getenv("OPENAI_API_KEY"),
            temperature=0.2
        )
    elif provider == "google":
        print("Using Google Gemini as LLM provider")
        return ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0.2
        )
    elif provider == "groq":
        print("Using Groq as LLM provider")
        return ChatGroq(
            model="llama-3.3-70b-versatile",
            api_key=os.getenv("GROQ_API_KEY"),
            temperature=0.2
        )
        
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")