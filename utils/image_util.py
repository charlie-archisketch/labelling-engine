import os
from typing import Any

from urllib.parse import urlparse

import requests


def infer_image_format(url: str, content_type: str | None) -> str:
    if content_type and "image/" in content_type:
        fmt = content_type.split("/")[1].split(";")[0].strip().lower()
    else:
        path = urlparse(url).path
        ext = os.path.splitext(path)[1].lower().lstrip(".")
        fmt = ext or "png"

    if fmt == "jpg":
        fmt = "jpeg"
    return fmt

def get_image_from_url(url: str) -> tuple[str, bytes | Any]:
    resp = requests.get(url)
    resp.raise_for_status()
    image = resp.content
    content_type = resp.headers.get("content-type")
    fmt = infer_image_format(url, content_type)

    return fmt, image