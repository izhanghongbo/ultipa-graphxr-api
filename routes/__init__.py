from fastapi import APIRouter
from .ultipa import router as ultipa_router

api_router = APIRouter()
api_router.include_router(ultipa_router, prefix="/ultipa", tags=["ultipa"])