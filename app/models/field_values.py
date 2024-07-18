import uuid

from ..extensions import db


class Field(db.Model):
    id= db.Column(db.String,primary_key=True, default=lambda : str(uuid.uuid4()))
    binding_name = db.Column(db.String,nullable=True)
    coordinates= db.Column(db.JSON,nullable=True)
    document_id= db.Column(db.String, db.ForeignKey('document.id'), nullable=False)
    document=db.relationship("Document",back_populates="fields")

    def __repr__(self):
        return '<Field id={}, binding_name={}, document_id={}>'.format(self.id, self.binding_name, self.document_id)