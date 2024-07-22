import uuid
from ..extensions import db


class Fields(db.Model):
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    binding_name = db.Column(db.String, nullable=True)
    coordinates = db.Column(db.JSON, nullable=True)
    required_field = db.Column(db.Boolean, nullable=False, default=True)

    document_type_id = db.Column(db.String, db.ForeignKey('document_type.id'), nullable=False, unique=False)
    document_type = db.relationship('DocumentType', back_populates='fields')

    field_document_mapping = db.relationship("FieldDocumentMapping", back_populates="fields",
                                             uselist=False)
    def __repr__(self):
        return '<Field id={}, binding_name={}>'.format(self.id, self.binding_name)
