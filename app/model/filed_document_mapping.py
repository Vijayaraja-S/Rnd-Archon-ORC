import uuid

from ..extensions import db


class FieldDocumentMapping(db.Model):
    __table_name__ = 'field_document_mapping'
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    value = db.Column(db.String, nullable=False)

    document_id = db.Column(db.String, db.ForeignKey('document.id'), nullable=False)
    document = db.relationship('Document', back_populates="document")

    field_id = db.Column(db.String, db.ForeignKey('fields.id'), nullable=False)
    fields = db.relationship('Fields', back_populates="field")

