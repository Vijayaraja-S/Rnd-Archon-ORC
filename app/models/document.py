import uuid

from ..enums.document_status import DocumentStatus
from ..extensions import db

from datetime import datetime
from sqlalchemy import DateTime


class Document(db.Model):
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    image_content = db.Column(db.Text, nullable=True)
    image_name = db.Column(db.String, nullable=True)
    status = db.Column(db.Enum(DocumentStatus), nullable=True)
    created_date = db.Column(DateTime, default=datetime.utcnow)
    modified_date = db.Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    document_type_id = db.Column(db.String, db.ForeignKey('document_type.id'), unique=False, nullable=False)

    field_document_mapping = db.Column(db.String, db.ForeignKey('field_document_mapping.id'), unique=False, nullable=False)




    def __repr__(self):
        return '<DocumentType id={}, template_name={}>'.format(self.id, self.template_name)
