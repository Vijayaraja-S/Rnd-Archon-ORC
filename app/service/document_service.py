from ..enums.document_status import DocumentStatus
from ..extensions import db
from ..model.beans import ImageDetails
from ..model.document import Document
from ..model.beans.request_bean import DocumentRequestBean


class DocumentService:

    @staticmethod
    def save_document(doc: ImageDetails, document_type_id):
        document = Document(image_content=doc.image_content,
                            image_name=doc.image_name,
                            status=DocumentStatus.PROCESSED,
                            document_type_id=document_type_id)
        db.session.add(document)
        db.session.commit()
        return document

    @staticmethod
    def get_document(document_id):
        return Document.query.get(document_id)

    @staticmethod
    def delete_document(document_id):
        document = Document.query.get(document_id)
        if document:
            db.session.delete(document)
            db.session.commit()
        return document

    @staticmethod
    def save_document_info(doc: DocumentRequestBean, document_type_id):
        document = Document(image_content=doc.image_content,
                            image_name=doc.image_name,
                            status=DocumentStatus.PROCESSED,
                            document_type_id=document_type_id)
        db.session.add(document)
        db.session.commit()
        return document
