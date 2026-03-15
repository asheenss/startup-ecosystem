from fastapi import APIRouter

router = APIRouter()


@router.get("/status")
async def ai_status():
    return {"status": "ready", "message": "Use /api/pitch/* for the production pitch analysis pipeline."}
