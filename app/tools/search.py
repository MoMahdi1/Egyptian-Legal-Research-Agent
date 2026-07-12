import logging
import os
from typing import List, Dict, Any

from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

logger = logging.getLogger(__name__)

# ==========================================================
# Tavily Client
# ==========================================================

client = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)

# ==========================================================
# Web Search
# ==========================================================

def web_search(
    query: str,
    max_results: int = 5
) -> List[Dict[str, Any]]:
    """
    Search the web using Tavily.

    Returns:
        List of documents compatible with the Retriever pipeline.
    """

    try:

        logger.info(f"Searching Tavily: {query}")

        response = client.search(
            query=query,
            max_results=max_results,
            search_depth="advanced"
        )

        formatted_results = []

        for item in response.get("results", []):

            score = item.get("score", 0)

            # Ignore weak results
            if score < 0.50:
                continue

            formatted_results.append(
                {
                    "content": item.get("content", "")[:1000],
                    "score": float(score),
                    "metadata": {
                        "title": item.get("title", "Unknown"),
                        "url": item.get("url", ""),
                        "source": "web"
                    }
                }
            )

        logger.info(
            f"Tavily returned {len(formatted_results)} useful results."
        )

        return formatted_results

    except Exception as e:

        logger.exception("Tavily Search Failed")

        return []