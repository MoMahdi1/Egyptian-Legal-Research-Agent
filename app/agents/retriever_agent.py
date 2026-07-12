from typing import Dict, Any, List

from app.tools.retriever import vectorstore
from app.tools.search import web_search
from app.agents.reranker import rerank_documents

MIN_RELEVANT_DOCS = 2
MAX_SCORE_THRESHOLD = 0.30
TOP_K = 5


def retriever_agent(queries: List[str]) -> Dict[str, Any]:
    """
    Multi-Query Corrective RAG

    Flow:
    1. Search Chroma using all generated queries.
    2. Merge retrieved documents.
    3. Remove duplicates.
    4. Rerank once.
    5. If retrieval quality is weak -> Web Search + Rerank.
    """

    try:

        print("\n========== MULTI QUERY RETRIEVAL ==========")

        retrieved_docs = []

        # -----------------------------
        # Search Chroma
        # -----------------------------
        for query in queries:

            print(f"\nSearching: {query}")

            docs_with_scores = vectorstore.similarity_search_with_score(
                query=query,
                k=TOP_K
            )

            for doc, score in docs_with_scores:

                print(f"Similarity Score: {score:.4f}")

                if score > MAX_SCORE_THRESHOLD:
                    continue

                retrieved_docs.append({
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "score": float(score)
                })

        # -----------------------------
        # Remove Duplicates
        # -----------------------------
        unique_docs = {}

        for doc in retrieved_docs:

            key = (
                doc["metadata"].get("source", "")
                + "_"
                + str(doc["metadata"].get("page", ""))
                + "_"
                + doc["content"][:150]
            )

            if key not in unique_docs:
                unique_docs[key] = doc

        filtered_docs = list(unique_docs.values())

        print(f"\nUnique Documents: {len(filtered_docs)}")

        # -----------------------------
        # Local Retrieval Success
        # -----------------------------
        if len(filtered_docs) >= MIN_RELEVANT_DOCS:

            print("\nRunning CrossEncoder Reranker...")

            reranked_docs = rerank_documents(
                query=queries[0],
                documents=filtered_docs,
                top_k=TOP_K
            )

            print("\n========== FINAL RANK ==========")

            for i, doc in enumerate(reranked_docs, 1):

                print(
                    f"[{i}] "
                    f"Similarity={doc['score']:.4f} | "
                    f"Rerank={doc['rerank_score']:.4f}"
                )

            return {
                "source": "documents",
                "results": reranked_docs,
                "fallback_used": False,
                "retrieved_count": len(filtered_docs)
            }

        # -----------------------------
        # Web Fallback
        # -----------------------------
        print("\nLocal retrieval weak -> Running Web Search")

        web_results = []

        for query in queries:
            web_results.extend(web_search(query))

        all_results = filtered_docs + web_results

        reranked_docs = rerank_documents(
            query=queries[0],
            documents=all_results,
            top_k=TOP_K
        )

        return {
            "source": "web",
            "results": reranked_docs,
            "fallback_used": True,
            "retrieved_count": len(filtered_docs)
        }

    except Exception as e:

        print(f"\n[Retriever Error] {e}")

        return {
            "source": "error",
            "results": [],
            "fallback_used": False,
            "retrieved_count": 0,
            "error": str(e)
        }