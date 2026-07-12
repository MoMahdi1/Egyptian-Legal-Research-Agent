import logging
from typing import Any, Dict, List

from sentence_transformers import CrossEncoder

logger = logging.getLogger(__name__)

# Load the reranker model once when the application starts
reranker_model = CrossEncoder(
    "cross-encoder/mmarco-mMiniLMv2-L12-H384-v1"
)


def rerank_documents(
    query: str,
    documents: List[Dict[str, Any]],
    top_k: int = 3,
) -> List[Dict[str, Any]]:
    """
    Rerank retrieved documents using a CrossEncoder model.

    Args:
        query: User search query.
        documents: Retrieved documents.
        top_k: Number of documents to return.

    Returns:
        Top reranked documents.
    """

    if not documents:
        return []

    # Pair each document with the query
    pairs = [
        (query, doc["content"])
        for doc in documents
    ]

    try:
        # Predict relevance scores
        scores = reranker_model.predict(pairs)

    except Exception as e:
        logger.exception("Reranker failed.")
        return documents[:top_k]

    ranked_docs = []

    # Create new dictionaries instead of modifying originals
    for doc, score in zip(documents, scores):

        ranked_docs.append({
            **doc,
            "rerank_score": float(score)
        })

    # Sort by reranker score (highest first)
    ranked_docs.sort(
        key=lambda x: x["rerank_score"],
        reverse=True
    )

    return ranked_docs[:top_k]