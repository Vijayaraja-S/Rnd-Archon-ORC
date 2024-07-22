from ..models.document_type import DocumentType
from ..extensions import db
from ..models.beans import RequestBean
from ..services.document_service import DocumentService


class DocumentTypeService:

    @staticmethod
    def create_document_type(request_bean: RequestBean):
        try:
            name = request_bean.template_name
            document_type = DocumentType(template_name=name)
            db.session.add(document_type)
            db.session.commit()
            DocumentService.save_document_info_init(request_bean, document_type)
            return document_type
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_document_type(document_type_id: str) -> DocumentType:
        return DocumentType.query.get(document_type_id)

    @staticmethod
    def update_document_type(document_type_id: str, template_name: str = None) -> DocumentType:
        try:
            document_type = DocumentType.query.get(document_type_id)
            if document_type:
                if template_name is not None:
                    document_type.template_name = template_name
                db.session.commit()
            return document_type
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_document_type(document_type_id: str) -> DocumentType:
        try:
            document_type = DocumentType.query.get(document_type_id)
            if document_type:
                db.session.delete(document_type)
                db.session.commit()
            return document_type
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def filter_document_types(template_name_filter: str):
        try:
            filter_pattern = '%{}%'.format(template_name_filter)
            return DocumentType.query.filter(DocumentType.template_name.like(filter_pattern)).all()
        except Exception as e:
            raise e
