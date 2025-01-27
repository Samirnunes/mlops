from typing import Dict

from fastapi import APIRouter

router = APIRouter(prefix="/v1/health", tags=["health"])


@router.get("")
async def get_health() -> Dict:
    return {"status": "operational"}
