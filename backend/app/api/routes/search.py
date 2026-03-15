from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.services.search_service import SearchService

router = APIRouter()

@router.get("/{id}/similar")
async def get_similar_startups(id: int, limit: int = 5, search_service: SearchService = Depends(SearchService)):
    """
    Retrieve startups similar to the one specified by ID.
    """
    results = search_service.find_similar_startups(id, limit=limit)
    if not results and limit > 0:
        # This could mean the startup doesn't exist or has no embeddings
        return []
    return results
