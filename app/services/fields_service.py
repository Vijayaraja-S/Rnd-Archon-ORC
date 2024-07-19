import json
from ..extensions import db
from ..models import DocumentType, Fields
from ..models.beans import RequestBean

from typing import List


class FieldsService:
    @staticmethod
    def save_fields_info(request_bean: RequestBean, document_type: DocumentType):
        try:
            field_details = request_bean.field_details
            for field in field_details:
                position = field.position.model_dump()
                dumps = json.dumps(position)
                fields = Fields(
                    binding_name=field.binding_name,
                    coordinates=dumps,
                    document_type_id=document_type.id
                )
                db.session.add(fields)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_fields_by_doc_type(document_type_id: str) -> List[Fields]:
        return Fields.query.filter_by(document_type_id=document_type_id).all()
