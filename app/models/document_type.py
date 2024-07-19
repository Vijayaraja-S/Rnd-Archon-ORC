import uuid

from ..extensions import db


class DocumentType(db.Model):
    # __tablename__ = 'document_type'
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    template_name = db.Column(db.String, nullable=True)
    document = db.relationship('Document', back_populates='document_type', lazy='dynamic')
    field = db.relationship('Fields', back_populates='document_type', lazy='dynamic')

    def __repr__(self):
        return '<DocumentType id={}, template_name={}>'.format(self.id, self.template_name)
