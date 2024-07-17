from ..models.document_type import DocumentType

from ..extensions import db


class DocumentTypeService:

    @staticmethod
    def create_document_type(template_name):
        document_type = DocumentType(template_name=template_name)
        db.session.add(document_type)
        db.session.commit()
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
