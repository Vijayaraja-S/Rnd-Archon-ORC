import uuid
from datetime import datetime
from sqlalchemy import DateTime
from ..enums.document_status import DocumentStatus
from ..extensions import db


class Document(db.Model):
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    image_content = db.Column(db.Text, nullable=True)
    image_name = db.Column(db.String, nullable=True)
    status = db.Column(db.Enum(DocumentStatus), nullable=True)
    created_date = db.Column(DateTime, default=datetime.utcnow)
    modified_date = db.Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    document_type_id = db.Column(db.String, db.ForeignKey('document_type.id'), unique=False, nullable=False)
    document_type = db.relationship('DocumentType', back_populates='documents')

    field_document_mappings = db.relationship('FieldDocumentMapping', back_populates='document',
                                              lazy='select', cascade='all, delete-orphan')

    def __repr__(self):
        return '<Document id={}, image_name={}>'.format(self.id, self.image_name)
