from fastapi import APIRouter

from schemas.label import CreateLabelRequest, NameResponse, TypeResponse, DescriptionResponse, TagsResponse
from service import label_service

router = APIRouter()

@router.post("/name/generate", response_model=NameResponse)
async def generate_product_name(request: CreateLabelRequest):
    return label_service.generate_product_name(request)

@router.post("/type/generate", response_model=TypeResponse)
async def generate_product_type(request: CreateLabelRequest) -> TypeResponse:
    return label_service.generate_product_type(request)

@router.post("/tags/generate", response_model=TagsResponse)
async def generate_product_tags(request: CreateLabelRequest) -> TagsResponse:
    return label_service.generate_product_tags(request)

@router.post("/description/generate", response_model=DescriptionResponse)
async def generate_product_description(request: CreateLabelRequest) -> DescriptionResponse:
    return label_service.generate_product_description(request)