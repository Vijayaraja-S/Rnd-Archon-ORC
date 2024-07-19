from typing import List

from pydantic import BaseModel


class Position(BaseModel):
    x: int
    y: int
    width: int
    height: int


class ImageDetails(BaseModel):
    image_content: str
    image_name: str


class FieldDetails(BaseModel):
    binding_name: str
    position: Position


class RequestBean(BaseModel):
    template_name: str
    image_details: List[ImageDetails]
    field_details: List[FieldDetails]


class FieldDetailsBuilder(BaseModel):
    id: str
    binding_name: str
    position: Position
