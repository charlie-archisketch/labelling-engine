import json

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


def _extract_tool_input(resp: dict, tool_name: str, key: str):
    contents = resp.get("output", {}).get("message", {}).get("content", [])
    for item in contents:
        if isinstance(item, dict) and item.get("toolUse"):
            tool_use = item["toolUse"]
            if tool_use.get("name") == tool_name:
                return tool_use.get("input", {}).get(key)
    return None


def generate_product_name(request: CreateLabelRequest) -> NameResponse:
    fmt, image = image_util.get_image_from_url(str(request.image_url))

    resp = bedrock.converse(
        modelId="us.amazon.nova-pro-v1:0",
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
    name = _extract_tool_input(resp, "generate_furniture_name", "name")

    return NameResponse(name=name)


def generate_product_type(request: CreateLabelRequest) -> TypeResponse:
    fmt, image = image_util.get_image_from_url(str(request.image_url))

    resp = bedrock.converse(
        modelId="us.amazon.nova-pro-v1:0",
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
    type_str = _extract_tool_input(resp, "generate_furniture_type", "type")
    if not type_str:
        raise RuntimeError("유형 생성 결과를 파싱하지 못했습니다.")
    try:
        type_value = EditorType[type_str]
    except KeyError:
        raise RuntimeError(f"알 수 없는 유형: {type_str}")
    return TypeResponse(type=type_value)


def generate_product_tags(request: CreateLabelRequest) -> TagsResponse:
    fmt, image = image_util.get_image_from_url(str(request.image_url))

    resp = bedrock.converse(
        modelId="us.amazon.nova-pro-v1:0",
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
    tags = _extract_tool_input(resp, "generate_furniture_tags", "tags") or []
    return TagsResponse(tags=tags)


def generate_product_description(request: CreateLabelRequest) -> DescriptionResponse:
    fmt, image = image_util.get_image_from_url(str(request.image_url))

    resp = bedrock.converse(
        modelId="us.amazon.nova-pro-v1:0",
        system=SYSTEM_PROMPT,
        messages=[{
            "role": "user",
            "content": [
                {"text": USER_PROMPT_TEMPLATE.format(**_safe_prompt_values(request), prompt="이 정보를 바탕으로 가구의 설명을 상세히 생성해줘")},
                {"image": {"format": fmt, "source": {"bytes": image}}},
            ],
        }],
        toolConfig={
            "tools": GENERATE_DESCRIPTION_TOOL,
            "toolChoice": {"tool": {"name": "generate_furniture_description"}},
        },
    )

    print(json.dumps(resp, ensure_ascii=False, indent=2))
    description = _extract_tool_input(resp, "generate_furniture_description", "description")

    return DescriptionResponse(description=description)
