from flask import Blueprint, request, jsonify
from ..services.document_type_service import DocumentTypeService
import logging

document_type_bp = Blueprint('document_type_bp', __name__)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@document_type_bp.route('/document_types', methods=['POST'])
def create_document_type():
    data = request.get_json()
    template_name = data.get('template_name')
    if not template_name:
        return jsonify({'error': 'Template name is required'}), 400

    document_type = DocumentTypeService.create_document_type(template_name)
    return jsonify({'id': document_type.id, 'template_name': document_type.template_name}), 201


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


@document_type_bp.route('/document_types', methods=['GET'])
def filter_document_types():
    template_name_filter = request.args.get('template_name')
    if not template_name_filter:
        return jsonify({'error': 'Template name filter is required'}), 400

    try:
        document_types = DocumentTypeService.filter_document_types(template_name_filter)
        if not document_types:
            return jsonify({'error': 'No document types found with template name containing "{}"'
                           .format(template_name_filter)}), 404

        result = [{
            'id': doc.id,
            'template_name': doc.template_name
        } for doc in document_types]

        return jsonify(result), 200
    except Exception as e:
        logger.error("Error occurred while filtering document types: {}".format(str(e)))
        return jsonify({'error': 'Internal server error'}), 500

