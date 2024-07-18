from ..models.document_type import DocumentType

from ..extensions import db
from ..models.beans import RequestBean
from ..services.document_service import DocumentService


class DocumentTypeService:

    @staticmethod
    def create_document_type(request_bean: RequestBean):
        name = request_bean.template_name
        document_type = DocumentType(template_name=name)
        db.session.add(document_type)
        db.session.commit()
        DocumentService.save_document_info(request_bean, document_type)
        return document_type

    @staticmethod
    def get_document_type(document_type_id):
        return DocumentType.query.get(document_type_id)

    @staticmethod
    def update_document_type(document_type_id, template_name=None):
        document_type = DocumentType.query.get(document_type_id)
        if document_type:
            if template_name is not None:
                document_type.template_name = template_name
            db.session.commit()
        return document_type

    @staticmethod
    def delete_document_type(document_type_id):
        document_type = DocumentType.query.get(document_type_id)
        if document_type:
            db.session.delete(document_type)
            db.session.commit()
        return document_type

    @staticmethod
    def filter_document_types(template_name_filter):
        filter_pattern = '%{}%'.format(template_name_filter)
        return DocumentType.query.filter(DocumentType.template_name.like(filter_pattern)).all()
