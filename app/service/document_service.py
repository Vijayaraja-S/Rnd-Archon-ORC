import json
import math
from typing import List, Dict
from uuid import UUID

from ..enums.document_status import DocumentStatus
from ..extensions import db
from ..model.beans.request_bean import DocumentRequestBean, ImageDetails
from ..model.beans.response_bean import FieldInfo, Position, ResultsInfoResponse, DocumentInfo, DocumentResponseBean
from ..model.document import Document
from ..model.fields import Fields
from ..model.filed_document_mapping import FieldDocumentMapping
from ..service.document_type_service import DocumentTypeService


class DocumentService:

    @staticmethod
    def save_document(doc: ImageDetails, document_type_id: str) -> Document:
        try:

            if DocumentService.check_document_exists(doc.image_name):
                raise ValueError(f'Document with name {doc.image_name} already exists')

            document = Document(
                image_content=doc.image_content,
                image_name=doc.image_name,
                status=DocumentStatus.PROCESSED,
                document_type_id=document_type_id
            )
            db.session.add(document)
            db.session.commit()
            return document
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_document_response(document_id):
        results, fields, document = DocumentService.get_document(document_id)

        def parse_coordinates(coordinates):
            if isinstance(coordinates, str):
                try:
                    return json.loads(coordinates)
                except json.JSONDecodeError:
                    return {}
            return coordinates or {}

        def create_field_info(result, field):
            coordinates = parse_coordinates(field.coordinates)
            return FieldInfo(
                bindingName=field.binding_name,
                position=Position(
                    x=coordinates.get('x', 0),
                    y=coordinates.get('y', 0),
                    width=coordinates.get('width', 0),
                    height=coordinates.get('height', 0)
                ),
                value=result.value,
                accuracy=result.accuracy
            )

        if document:
            results_response = [ResultsInfoResponse(id=UUID(result.id), value=result.value) for result in results]
            field_id_map = {field.id: field for field in fields}
            fields_response = [create_field_info(result, field_id_map.get(result.field_id, {})) for result in results]

            document_response = DocumentInfo(
                id=document.id,
                image_name=document.image_name,
                image_content=document.image_content,
                createdAt=document.created_date.isoformat(),
                modifiedAt=document.modified_date.isoformat() if document.modified_date else None,
                status=document.status
            )

            return DocumentResponseBean(
                document_info=[document_response],
                document_type_id=document.document_type_id,
                fields=fields_response,
                results=results_response
            )

        # Return an empty DocumentResponseBean if no document is found
        return DocumentResponseBean(
            document_info=[],
            document_type_id='',
            fields=[],
            results=[]
        )

    @staticmethod
    def get_document(document_id: str):
        results_info = FieldDocumentMapping.query.filter_by(document_id=document_id).all()
        if results_info is None:
            print(f"No record found in FieldDocumentMapping with document_id: {document_id}")
        else:
            print("results_info:", results_info)

        field_ids = [result.field_id for result in results_info] if results_info else []

        fields_info = Fields.query.filter(Fields.id.in_(field_ids)).all()
        if fields_info is None:
            print(f"No fields found in Fields table with document_id: {document_id}")
        else:
            print("fields_info:", fields_info)

        document_info = Document.query.get(document_id)

        if document_info is None:
            print(f"Document with id {document_id} does not exist")
        else:
            print("document_info:", document_info)

        return results_info, fields_info, document_info

    @staticmethod
    def get_all_documents(page: int, per_page: int, image_name: str, status: str) -> Dict[str, any]:
        try:
            offset = (page - 1) * per_page

            query = Document.query

            if image_name:
                query = query.filter(Document.image_name.ilike(f'%{image_name}%'))
            if status:
                query = query.filter(Document.status == status)

            total_documents = query.count()

            documents = query.offset(offset).limit(per_page).all()

            response = {
                'documents': [{
                    'id': doc.id,
                    'image_content': doc.image_content,
                    'image_name': doc.image_name,
                    'created_date': doc.created_date,
                    'modified_date': doc.modified_date,
                    'status': doc.status.value,
                    'document_type_id': doc.document_type_id
                } for doc in documents],
                'total_documents': total_documents,
                'page': page,
                'per_page': per_page,
                'total_pages': math.ceil(total_documents / per_page)
            }

            return response
        except Exception as e:
            print(f"An error occurred: {e}")
            return {
                'documents': [],
                'total_documents': 0,
                'page': page,
                'per_page': per_page,
                'total_pages': 0
            }

    @staticmethod
    def delete_document(document_id: str) -> Document:
        document = Document.query.get(document_id)
        if document:
            try:
                db.session.delete(document)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise e
        return document

    @staticmethod
    def get_doc_by_status(status: DocumentStatus) -> List[Document]:
        try:
            status_all = db.session.query(Document).filter(Document.status == status).all()
            return status_all
        except Exception as e:
            raise e

    @staticmethod
    def save_document_info(doc: DocumentRequestBean, document_type_id):
        try:
            document_type = DocumentTypeService.get_document_type(document_type_id)

            document = Document(
                image_content=doc.image_content,
                image_name=doc.image_name,
                status=DocumentStatus.SCHEDULED,
                document_type_id=document_type_id,
                document_type=document_type
            )

            db.session.add(document)
            db.session.commit()
            return document

        except Exception as e:
            db.session.rollback()
            print(f"Error creating document: {e}")
            raise

    @staticmethod
    def check_document_exists(image_name: str) -> bool:
        return Document.query.filter_by(image_name=image_name).first()
