import json

from ..extensions import db
from ..model import DocumentType, Fields
from ..model.beans import RequestBean


class FieldsService:
    @staticmethod
    def save_fields_info(request_bean: RequestBean, document_type: DocumentType):
        field_details = request_bean.field_details
        for field in field_details:
            position = field.position.model_dump()
            dumps = json.dumps(position)
            fields = Fields(binding_name=field.binding_name,
                            coordinates=dumps,
                            document_type_id=document_type.id
                            )
            db.session.add(fields)
            db.session.commit()
