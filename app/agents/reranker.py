from sentence_transformers import CrossEncoder


## Load reranker model 

reranker_model = CrossEncoder(
    "cross-encoder/mmarco-mMiniLMv2-L12-H384-v1"
    )

def rerank_documents(query:str, documents: list, top_k: int =3):
    
    if not documents:
        return []
    
    # Pair the query with each document content
    pairs =[
        (query, doc["content"])
        for doc in documents
    ]
    
    # Predict relevance scores for each pair
    
    scores = reranker_model.predict(pairs)
    
    # Attach scores to documents
    
    ranked_docs =[]
    
    for doc , score in zip(documents, scores):
        
        doc["rerank_score"] = float(score)
        
        ranked_docs.append(doc)
        
        
    # Sort Decending by score
    
    ranked_docs = sorted(
        ranked_docs,
        key=lambda x: x["rerank_score"],
        reverse=True
    )
    
    return ranked_docs[:top_k]