from ..extensions import db

from ..models.filed_document_mapping import FieldDocumentMapping


class DocumentFieldService:
    @staticmethod
    def save_field_document_info(field_id, doc_id, value):
        try:
            field_document_mapping = FieldDocumentMapping(field_id=field_id, document_id=doc_id, value=value)
            db.session.add(field_document_mapping)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
