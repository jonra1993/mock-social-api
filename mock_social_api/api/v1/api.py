from fastapi import APIRouter
from mock_social_api.api.v1.endpoints import (
    instagram, tiktok
)

api_router = APIRouter()
api_router.include_router(instagram.router, prefix="/instagram", tags=["instagram"])
api_router.include_router(tiktok.router, prefix="/tiktok", tags=["tiktok"])
