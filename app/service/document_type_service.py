import math

from sqlalchemy.exc import SQLAlchemyError

from ..model.beans.response_bean import DocumentTypeInfo, DocumentInfoResponseBean
from ..model.document_type import DocumentType

from ..extensions import db
from ..model.beans import RequestBean
from ..service.document_service import DocumentService
from ..exception.exceptions import DatabaseError


class DocumentTypeService:

    @staticmethod
    def create_document_type(request_bean: RequestBean):
        name = request_bean.template_name
        document_type = DocumentType(template_name=name)
        db.session.add(document_type)
        db.session.commit()
        DocumentService.save_document_info_init(request_bean, document_type)
        return document_type

    @staticmethod
    def get_document_type(document_type_id: str):
        return DocumentType.query.get(document_type_id)

    @staticmethod
    def update_document_type(document_type_id, template_name=None):
        document_type = DocumentType.query.get(document_type_id)
        if document_type:
            if template_name is not None:
                document_type.template_name = template_name
            db.session.commit()
        return document_type

    @staticmethod
    def delete_document_type(document_type_id):
        document_type = DocumentType.query.get(document_type_id)
        if document_type:
            db.session.delete(document_type)
            db.session.commit()
        return document_type

    @staticmethod
    def filter_document_types(template_name_filter):
        filter_pattern = '%{}%'.format(template_name_filter)
        return DocumentType.query.filter(DocumentType.template_name.like(filter_pattern)).all()

    @staticmethod
    def get_templates_service(template_name=None, page=1, per_page=10):
        try:
            query = DocumentType.query

            if template_name:
                query = query.filter(DocumentType.template_name.ilike(f'%{template_name}%'))

            total_templates = query.count()

            templates = query.offset((page - 1) * per_page).limit(per_page).all()

            result = [DocumentTypeInfo(id=template.id, template_name=template.template_name) for template in templates]

            pagination = {
                'page': page,
                'per_page': per_page,
                'total_pages': math.ceil(total_templates / per_page),
                'total_templates': total_templates
            }

            response_bean = DocumentInfoResponseBean(response=result, pagination=pagination)

            return response_bean.model_dump(by_alias=True)

        except SQLAlchemyError as e:
            raise DatabaseError(f"Database query failed: {str(e)}")