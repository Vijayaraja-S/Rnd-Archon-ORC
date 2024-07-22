from typing import List

from ..enums.document_status import DocumentStatus
from ..extensions import db
from ..model.beans.request_bean import DocumentRequestBean, ImageDetails
from ..model.document import Document


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
        document = Document(image_content=doc.image_content,
                            image_name=doc.image_name,
                            status=DocumentStatus.PROCESSED,
                            document_type_id=document_type_id)
        db.session.add(document)
        db.session.commit()
        return document
