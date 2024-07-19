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
    required: bool


class TemplateRequestBean(BaseModel):
    template_name: str
    image_content: str
    field_details: List[FieldDetails]


class DocumentRequestBean(BaseModel):
    image_content: str
    image_name: str

