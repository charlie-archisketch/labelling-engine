import logging

import boto3
import json
from dotenv import load_dotenv

from core.constants import SYSTEM_PROMPT, GENERATE_NAME_TOOL, USER_PROMPT_TEMPLATE
from schemas.label import LabelCreateRequest, NameResponse
from utils import image_util

load_dotenv()

bedrock = boto3.client(service_name="bedrock-runtime", region_name="us-west-2")

def generate_product_name(request: LabelCreateRequest) -> NameResponse:
    fmt, image = image_util.get_image_from_url(request["image_url"])

    resp = bedrock.converse(
        modelId="us.amazon.nova-pro-v1:0",  # Amazon Nova Pro
        system=SYSTEM_PROMPT,
        messages=[{
            "role": "user",
            "content": [
                {"text": USER_PROMPT_TEMPLATE.format(
                    name=request.name,
                    type=request.type.name,
                    tags=", ".join(request.tags),
                    description=request.description,
                    prompt="이 정보를 바탕으로 가구의 설명을 생성해줘"
                )},
                {
                    "image": {
                        "format": fmt,
                        "source": {"bytes": image}
                    }
                }
            ]
        }],
        toolConfig={
            "tools": GENERATE_NAME_TOOL,
            "toolChoice": {
                "tool": {
                    "name": "generate_furniture_description",
                }
            }
        }
    )

    logging.info(json.dumps(
        resp,
        ensure_ascii=False,
        indent=2,
    ))

    return NameResponse(name=resp["output"]["messages"][0]["toolUse"]["input"]["tags"])