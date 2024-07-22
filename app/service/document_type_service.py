import math

from sqlalchemy.exc import SQLAlchemyError

from ..exception.exceptions import DatabaseError, ValidationError
from ..extensions import db
from ..model.beans.request_bean import TemplateRequestBean
from ..model.beans.response_bean import DocumentTypeInfo, DocumentInfoResponseBean
from ..model.document_type import DocumentType
from ..service.fields_service import FieldsService


class DocumentTypeService:

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
        try:
            document_type = DocumentType.query.get(document_type_id)
            if document_type:
                # template , fields , value
                db.session.delete(document_type)
                db.session.commit()
                return document_type
            return None
        except SQLAlchemyError as e:
            db.session.rollback()
            raise DatabaseError(f"Database query failed: {str(e)}")

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

    @staticmethod
    def create_template(template_data: TemplateRequestBean) -> DocumentType:
        try:
            new_template = DocumentType(
                template_name=template_data.template_name,
                image=template_data.image_content
            )
            db.session.add(new_template)
            db.session.commit()
            FieldsService.save_fields_info(template_data.field_details, new_template.id)
            return new_template
        except ValidationError as e:
            db.session.rollback()
            raise ValueError(f'Validation error: {e}')
        except Exception as e:
            db.session.rollback()
            raise ValueError(f'Database error: {e}')
