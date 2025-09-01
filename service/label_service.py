import json
import os

import boto3
from dotenv import load_dotenv

from core.constants import (
    SYSTEM_PROMPT,
    GENERATE_NAME_TOOL,
    GENERATE_TYPE_TOOL,
    GENERATE_TAGS_TOOL,
    GENERATE_DESCRIPTION_TOOL,
    USER_PROMPT_TEMPLATE,
)
from schemas.label import (
    CreateLabelRequest,
    NameResponse,
    TypeResponse,
    TagsResponse,
    DescriptionResponse,
    EditorType,
)
from utils import image_util

load_dotenv()

bedrock = boto3.client(service_name="bedrock-runtime", region_name="us-west-2")


def _safe_prompt_values(req: CreateLabelRequest) -> dict:
    return {
        "name": req.name or "",
        "type": req.type.name if req.type else "",
        "tags": ", ".join(req.tags or []),
        "description": req.description or "",
    }


def _extract_tool_input(resp: dict, field: str):
    return resp["output"]["message"]["content"][0]["toolUse"]["input"][field]


def generate_product_name(request: CreateLabelRequest) -> NameResponse:
    fmt, image = image_util.get_image_from_url(str(request.image_url))

    resp = bedrock.converse(
        modelId=os.getenv("BEDROCK_MODEL_ID"),
        system=SYSTEM_PROMPT,
        messages=[{
            "role": "user",
            "content": [
                {"text": USER_PROMPT_TEMPLATE.format(**_safe_prompt_values(request), prompt="이 정보를 바탕으로 가구의 이름을 생성해줘")},
                {"image": {"format": fmt, "source": {"bytes": image}}},
            ],
        }],
        toolConfig={
            "tools": GENERATE_NAME_TOOL,
            "toolChoice": {"tool": {"name": "generate_furniture_name"}},
        },
    )

    print(json.dumps(resp, ensure_ascii=False, indent=2))
    name = _extract_tool_input(resp, "name")

    return NameResponse(name=name)


def generate_product_type(request: CreateLabelRequest) -> TypeResponse:
    fmt, image = image_util.get_image_from_url(str(request.image_url))

    resp = bedrock.converse(
        modelId=os.getenv("BEDROCK_MODEL_ID"),
        system=SYSTEM_PROMPT,
        messages=[{
            "role": "user",
            "content": [
                {"text": USER_PROMPT_TEMPLATE.format(**_safe_prompt_values(request), prompt="이 정보를 바탕으로 가구의 유형을 분류해줘")},
                {"image": {"format": fmt, "source": {"bytes": image}}},
            ],
        }],
        toolConfig={
            "tools": GENERATE_TYPE_TOOL,
            "toolChoice": {"tool": {"name": "generate_furniture_type"}},
        },
    )

    print(json.dumps(resp, ensure_ascii=False, indent=2))
    type_str = str(_extract_tool_input(resp, "type"))
    type_value = EditorType(type_str)

    return TypeResponse(type=type_value)


def generate_product_tags(request: CreateLabelRequest) -> TagsResponse:
    fmt, image = image_util.get_image_from_url(str(request.image_url))

    resp = bedrock.converse(
        modelId=os.getenv("BEDROCK_MODEL_ID"),
        system=SYSTEM_PROMPT,
        messages=[{
            "role": "user",
            "content": [
                {"text": USER_PROMPT_TEMPLATE.format(**_safe_prompt_values(request), prompt="이 정보를 바탕으로 가구의 태그를 생성해줘")},
                {"image": {"format": fmt, "source": {"bytes": image}}},
            ],
        }],
        toolConfig={
            "tools": GENERATE_TAGS_TOOL,
            "toolChoice": {"tool": {"name": "generate_furniture_tags"}},
        },
    )

    print(json.dumps(resp, ensure_ascii=False, indent=2))
    tags = _extract_tool_input(resp, "tags")

    return TagsResponse(tags=tags)


def generate_product_description(request: CreateLabelRequest) -> DescriptionResponse:
    fmt, image = image_util.get_image_from_url(str(request.image_url))

    resp = bedrock.converse(
        modelId=os.getenv("BEDROCK_MODEL_ID"),
        system=SYSTEM_PROMPT,
        messages=[{
            "role": "user",
            "content": [
                {"text": USER_PROMPT_TEMPLATE.format(**_safe_prompt_values(request), prompt="이 정보를 바탕으로 가구를 상세히 설명해줘")},
                {"image": {"format": fmt, "source": {"bytes": image}}},
            ],
        }],
        toolConfig={
            "tools": GENERATE_DESCRIPTION_TOOL,
            "toolChoice": {"tool": {"name": "generate_furniture_description"}},
        },
    )

    print(json.dumps(resp, ensure_ascii=False, indent=2))
    description = _extract_tool_input(resp, "description")

    return DescriptionResponse(description=description)
