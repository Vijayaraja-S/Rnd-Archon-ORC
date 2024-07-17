import uuid

from ..extensions import db


class Document(db.Model):
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    template_image = db.Column(db.Text, nullable=True)
    columns = db.Column(db.JSON, nullable=True)
    document_type_id = db.Column(db.String, db.ForeignKey('document_type.id'), unique=False, nullable=False)
    document_type = db.relationship("DocumentType", back_populates="document")

    def __repr__(self):
        return f'<Document id={self.id}, template_image={self.template_name} >'
