from typing import List
from pydantic import BaseModel


class DocumentTypeInfo(BaseModel):
    id: str
    template_name: str


class DocumentInfoResponseBean(BaseModel):
    response: List[DocumentTypeInfo]
    pagination: dict


class DocumentInfo(BaseModel):
    id: str
    image_name: str
    image_content: str
    createdAt: str
    modifiedAt: str
    status: str


class DocumentResponse(BaseModel):
    document_info: List[DocumentInfo]


class Position(BaseModel):
    x: int
    y: int
    width: int
    height: int


class FieldInfo(BaseModel):
    bindingName: str
    position: Position
    value: str
    accuracy: str


class FieldInfoResponseBean(BaseModel):
    response: List[FieldInfo]
