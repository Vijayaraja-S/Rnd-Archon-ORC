from ..models.document import Document

from ..extensions import db


class DocumentService:

    @staticmethod
    def create_document(template_image, columns):
        document = Document(template_image=template_image, columns=columns)
        db.session.add(document)
        db.session.commit()
        return document

    @staticmethod
    def get_document(document_id):
        return Document.query.get(document_id)

    @staticmethod
    def update_document(document_id, template_image=None, columns=None):
        document = Document.query.get(document_id)
        if document:
            if template_image is not None:
                document.template_image = template_image
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
