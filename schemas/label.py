from enum import Enum

from pydantic import BaseModel


class EditorType(str, Enum):
    FLOOR_ITEM = "Floor Item"
    STANDING_ITEM = "Standing Item"
    WALL_ITEM = "Wall Item"
    CEILING_ITEM = "Ceiling Item"
    SWING_DOOR = "Swing Door"
    SLIDING_DOOR = "Sliding Door"
    FOLDING_DOOR = "Folding Door"
    GARAGE_DOOR = "Garage Door"
    SWING_WINDOW = "Swing Window"
    SLIDING_WINDOW = "Sliding Window"
    FOLDING_WINDOW = "Folding Window"
    STANDARD_WINDOW = "Standard Window"
    SPACE = "Space"

class LabelCreateRequest(BaseModel):
    image_url: str
    name: str
    type: EditorType
    tags: list[str]
    description: str

class NameResponse(BaseModel):
    name: str

class TypeResponse(BaseModel):
    type: EditorType

class TagsResponse(BaseModel):
    tags: list[str]

class DescriptionResponse(BaseModel):
    description: str