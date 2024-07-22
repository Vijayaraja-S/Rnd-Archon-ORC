import uuid
from ..extensions import db


class DocumentType(db.Model):
    __tablename__ = 'document_type'
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    template_name = db.Column(db.String, nullable=True)
    image = db.Column(db.Text, nullable=True)

    documents = db.relationship('Document', back_populates='document_type', lazy='dynamic')
    fields = db.relationship('Fields', back_populates='document_type', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return '<DocumentType id={}, template_name={}>'.format(self.id, self.template_name)
