from ..models import DocumentType
from ..models.document import Document
from ..models.beans import RequestBean
from ..enums.document_status import DocumentStatus

from ..services.fields_service import FieldsService
from ..extensions import db


class DocumentService:

    @staticmethod
    def save_document_info(request_bean: RequestBean, document_type: DocumentType):
        for doc in request_bean.image_details:
            """need to add other fields"""
            document = Document(image_content=doc.image_content,
                                image_name=doc.image_name,
                                status=DocumentStatus.PROCESSED,
                                document_type=document_type,
                                document_type_id=document_type.id)
            db.session.add(document)
            db.session.commit()
        FieldsService.save_fields_info(request_bean, document_type)

        return ""

    @staticmethod
    def create_document(template):
        pass

    @staticmethod
    def get_document(document_id):
        return Document.query.get(document_id)

    @staticmethod
    def update_document(document_id, image_content=None, columns=None):
        document = Document.query.get(document_id)
        if document:
            if image_content is not None:
                document.template_image = image_content
            if columns is not None:
                document.columns = columns
            db.session.commit()
        return document

    @staticmethod
    def delete_document(document_id):
        document = Document.query.get(document_id)
        if document:
            db.session.delete(document)
            db.session.commit()
        return document
