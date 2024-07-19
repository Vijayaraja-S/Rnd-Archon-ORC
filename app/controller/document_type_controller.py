import logging

from flask import Blueprint, request, jsonify

from ..exception.exceptions import DatabaseError, ServiceError
from ..model.beans import RequestBean
from ..service.document_type_service import DocumentTypeService

document_type_bp = Blueprint('document_type_bp', __name__)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@document_type_bp.route('/document_types', methods=['POST'])
def create_document_type():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Template name is required'}), 400
    bean = RequestBean(**data)
    document_type = DocumentTypeService.create_document_type(bean)
    return jsonify({'id': document_type.id, 'template_name': document_type.template_name}), 201


@document_type_bp.route('/templates', methods=['GET'])
def get_templates():
    template_name = request.args.get('template_name', None)

    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
    except ValueError:
        return jsonify({"error": "Invalid page or per_page parameter"}), 400

    page = max(page, 1)
    per_page = max(per_page, 1)

    try:
        response_dict = DocumentTypeService.get_templates_service(template_name, page, per_page)
    except DatabaseError as e:
        return jsonify(e.to_dict()), e.error_code
    except ServiceError as e:
        logging.error(f"Service error: {str(e)}")
        return jsonify(e.to_dict()), e.error_code

    return jsonify(response_dict), 200


@document_type_bp.route('/document_types/<document_type_id>', methods=['GET'])
def get_document_type(document_type_id):
    try:
        document_type = DocumentTypeService.get_document_type(document_type_id)
        if document_type is None:
            return jsonify({'error': 'Document type not found'}), 404

        return jsonify({
            'id': document_type.id,
            'template_name': document_type.template_name
        }), 200
    except Exception as e:
        logger.error("Error occurred while getting DocumentType with id {}: {}".format(document_type_id, str(e)))
        return jsonify({'error': 'Internal server error'}), 500


@document_type_bp.route('/document_types/<document_type_id>', methods=['PUT'])
def update_document_type(document_type_id):
    data = request.get_json()
    template_name = data.get('template_name')

    document_type = DocumentTypeService.update_document_type(document_type_id, template_name)
    if document_type is None:
        return jsonify({'error': 'Document type not found'}), 404

    return jsonify({'id': document_type.id, 'template_name': document_type.template_name})


@document_type_bp.route('/document_types/<document_type_id>', methods=['DELETE'])
def delete_document_type(document_type_id):
    document_type = DocumentTypeService.delete_document_type(document_type_id)
    if document_type is None:
        return jsonify({'error': 'Document type not found'}), 404

    return jsonify({'result': 'Document type deleted'})

