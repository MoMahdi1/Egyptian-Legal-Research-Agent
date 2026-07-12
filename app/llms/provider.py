import os

from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_core.messages import BaseMessage

load_dotenv()


# ==========================
# Default LLM
# ==========================

def get_llm():

    if os.getenv("GROQ_API_KEY"):
        print("Using Groq")
        return ChatGroq(
            model="llama-3.3-70b-versatile",
            api_key=os.getenv("GROQ_API_KEY"),
            temperature=0.2,
        )

    elif os.getenv("GOOGLE_API_KEY"):
        print("Using Google Gemini")
        return ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0.2,
        )

    elif os.getenv("OPENAI_API_KEY"):
        print("Using OpenAI")
        return ChatOpenAI(
            model="gpt-4o-mini",
            api_key=os.getenv("OPENAI_API_KEY"),
            temperature=0.2,
        )

    raise RuntimeError("No LLM API key found.")


# ==========================
# Failover
# ==========================

def invoke_llm(llm, messages: list[BaseMessage]):

    providers = [

        (
            "google",
            lambda: ChatGoogleGenerativeAI(
                model="gemini-2.5-flash",
                api_key=os.getenv("GOOGLE_API_KEY"),
                temperature=0.2,
            ),
        ),

        (
            "groq",
            lambda: ChatGroq(
                model="llama-3.3-70b-versatile",
                api_key=os.getenv("GROQ_API_KEY"),
                temperature=0.2,
            ),
        ),

        (
            "openai",
            lambda: ChatOpenAI(
                model="gpt-4o-mini",
                api_key=os.getenv("OPENAI_API_KEY"),
                temperature=0.2,
            ),
        ),
    ]

    try:
        return llm.invoke(messages)

    except Exception as e:

        print(f"\nCurrent provider failed: {e}")

    current = os.getenv("LLM_PROVIDER", "google")

    for name, factory in providers:

        if name == current:
            continue

        try:

            print(f"Switching to {name}...")

            model = factory()

            os.environ["LLM_PROVIDER"] = name

            return model.invoke(messages)

        except Exception as e:

            print(f"{name} failed: {e}")

    raise RuntimeError("All LLM providers failed.")