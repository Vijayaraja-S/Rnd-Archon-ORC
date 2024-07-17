from flask import Blueprint, request, jsonify
from ..services.document_type_service import DocumentTypeService

document_type_bp = Blueprint('document_type_bp', __name__)


@document_type_bp.route('/document_types', methods=['POST'])
def create_document_type():
    data = request.get_json()
    template_name = data.get('template_name')
    if not template_name:
        return jsonify({'error': 'Template name is required'}), 400

    document_type = DocumentTypeService.create_document_type(template_name)
    return jsonify({'id': document_type.id, 'template_name': document_type.template_name}), 201


@document_type_bp.route('/document_types/<int:document_type_id>', methods=['GET'])
def get_document_type(document_type_id):
    document_type = DocumentTypeService.get_document_type(document_type_id)
    if document_type is None:
        return jsonify({'error': 'Document type not found'}), 404

    return jsonify({'id': document_type.id, 'template_name': document_type.template_name})


@document_type_bp.route('/document_types/<int:document_type_id>', methods=['PUT'])
def update_document_type(document_type_id):
    data = request.get_json()
    template_name = data.get('template_name')

    document_type = DocumentTypeService.update_document_type(document_type_id, template_name)
    if document_type is None:
        return jsonify({'error': 'Document type not found'}), 404

    return jsonify({'id': document_type.id, 'template_name': document_type.template_name})


@document_type_bp.route('/document_types/<int:document_type_id>', methods=['DELETE'])
def delete_document_type(document_type_id):
    document_type = DocumentTypeService.delete_document_type(document_type_id)
    if document_type is None:
        return jsonify({'error': 'Document type not found'}), 404

    return jsonify({'result': 'Document type deleted'})
