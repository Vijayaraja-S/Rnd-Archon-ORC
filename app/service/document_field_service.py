from ..extensions import db

from ..model.filed_document_mapping import FieldDocumentMapping


class DocumentFieldService:
    @staticmethod
    def save_field_document_info(field_id, doc_id, value, accuracy):
        try:
            accuracy = accuracy * 100
            field_document_mapping = FieldDocumentMapping(field_id=field_id, document_id=doc_id, value=value,
                                                          accuracy=accuracy)
            db.session.add(field_document_mapping)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
