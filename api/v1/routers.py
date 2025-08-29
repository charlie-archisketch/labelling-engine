from fastapi import APIRouter

from api.v1.endpoints import label

api_router = APIRouter()
api_router.include_router(label.router, prefix="/v1/labels", tags=["labels"])