import uuid

from ..extensions import db


class FieldDocumentMapping(db.Model):
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    value = db.Column(db.String, nullable=False)

    # document_id = db.Column(db.String, db.ForeignKey('document.id'), nullable=False)

    field_id = db.Column(db.String, db.ForeignKey('fields.id'), nullable=False)

    document_field = db.relationship("Document", back_populates="field_document_mapping", lazy='dynamic')

