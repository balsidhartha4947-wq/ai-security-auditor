from fastapi import APIRouter

from app.services.embedding_service import (
    create_embedding
)

from app.services.vector_service import (
    search_similar
)

router = APIRouter()


@router.get("/search")
def semantic_search(query: str):

    embedding = create_embedding(query)

    results = search_similar(embedding)

    return {
        "query": query,
        "results": results
    }