import uuid

from ..extensions import db


class FieldDocumentMapping(db.Model):
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    value = db.Column(db.String, nullable=False)
    accuracy = db.Column(db.Integer, nullable=False)

    document_id = db.Column(db.String, db.ForeignKey('document.id'), nullable=False, unique=False)
    document = db.relationship("Document", back_populates="field_document_mappings", lazy='select')

    field_id = db.Column(db.String, db.ForeignKey('fields.id'), nullable=False, unique=False)
    fields = db.relationship('Fields', back_populates='field_document_mapping')

    def __repr__(self):
        return '<FieldDocumentMapping id={}, value={}>'.format(self.id, self.value)
