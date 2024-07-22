from ..models import DocumentType
from ..models.beans import RequestBean, ImageDetails
from ..models.document import Document
from ..services.fields_service import FieldsService
from ..extensions import db
from ..enums.document_status import DocumentStatus
from typing import List


class DocumentService:

    @staticmethod
    def save_document_info_init(request_bean: RequestBean, document_type: DocumentType):
        try:
            for doc in request_bean.image_details:
                document = Document(
                    image_content=doc.image_content,
                    image_name=doc.image_name,
                    status=DocumentStatus.PROCESSED,
                    document_type_id=document_type.id
                )
                db.session.add(document)
            db.session.commit()
            FieldsService.save_fields_info(request_bean, document_type)
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def save_document(doc: ImageDetails, document_type_id: str) -> Document:
        try:
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
    def get_document(document_id: str) -> Document:
        return Document.query.get(document_id)

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
