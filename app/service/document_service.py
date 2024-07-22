from typing import List

from ..enums.document_status import DocumentStatus
from ..extensions import db
from ..model.beans.request_bean import DocumentRequestBean, ImageDetails
from ..model.document import Document
from ..service.document_type_service import DocumentTypeService


class DocumentService:

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
    def get_all_documents() -> List[Document]:
        try:
            documents = Document.query.all()
            return documents
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

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
