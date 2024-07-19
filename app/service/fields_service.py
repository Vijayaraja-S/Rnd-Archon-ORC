import json

from ..extensions import db
from ..model import Fields


class FieldsService:
    @staticmethod
    def save_fields_info(field_details: list, document_type_id):
        for field in field_details:
            position = field.position.model_dump()
            dumps = json.dumps(position)
            fields = Fields(binding_name=field.binding_name,
                            coordinates=dumps,
                            document_type_id=document_type_id
                            )
            db.session.add(fields)
            db.session.commit()
