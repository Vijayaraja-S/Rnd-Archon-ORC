import uuid

from ..extensions import db


class DocumentType(db.Model):
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    template_name = db.Column(db.String, nullable=True)
    document = db.relationship('Document', back_populates='document_type', lazy='dynamic')

    def __repr__(self):
        return f'<DocumentType id={self.id}, template_name={self.template_name}>'
