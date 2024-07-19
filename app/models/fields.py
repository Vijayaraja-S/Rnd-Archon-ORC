import uuid

from ..extensions import db


class Fields(db.Model):
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    binding_name = db.Column(db.String, nullable=True)
    coordinates = db.Column(db.JSON, nullable=True)

    document_type_id = db.Column(db.String, db.ForeignKey('document_type.id'), nullable=False, unique=False)

    field = db.relationship("FieldDocumentMapping", back_populates="fields", lazy='dynamic')

    def __repr__(self):
        return '<Field id={}, binding_name={}, document_id={}>'.format(self.id, self.binding_name, self.document_id)
