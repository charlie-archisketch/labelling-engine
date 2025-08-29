from fastapi import APIRouter

from schemas.label import LabelCreateRequest, NameResponse, TypeResponse, DescriptionResponse, TagsResponse
from service import label_service

router = APIRouter()

@router.post("/name/generate", response_model=NameResponse)
async def generate_product_name(request: LabelCreateRequest):
    return label_service.generate_product_name(request)

@router.post("/type/generate", response_model=TypeResponse)
async def generate_product_type(request: LabelCreateRequest) -> TypeResponse:
    pass

@router.post("/tags/generate", response_model=TagsResponse)
async def generate_product_tags(request: LabelCreateRequest) -> TagsResponse:
    pass

@router.post("/description/generate", response_model=DescriptionResponse)
async def generate_product_description(request: LabelCreateRequest) -> DescriptionResponse:
    pass