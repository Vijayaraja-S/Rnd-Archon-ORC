from ..services.document_service import DocumentService
from flask import Blueprint, request, jsonify

document_bp = Blueprint('document', __name__)


@document_bp.route('/documents', methods=['POST'])
def create_document():
    data = request.json
    template_image = data.get('template_image')

    if not template_image:
        return jsonify({'error': 'Template image is required'}), 400

    document = DocumentService.create_document(template_image)
    return jsonify({
        'id': document.id,
        'template_image': document.template_image,
        'columns': document.columns
    }), 201


@document_bp.route('/documents/<document_id>', methods=['GET'])
def get_document(document_id):
    document = DocumentService.get_document(document_id)
    if document:
        return jsonify({
            'id': document.id,
            'template_image': document.template_image,
            'columns': document.columns
        })
    return jsonify({'error': 'Document not found'}), 404


@document_bp.route('/documents/<document_id>', methods=['PUT'])
def update_document(document_id):
    data = request.json
    template_image = data.get('template_image')
    columns = data.get('columns')

    document = DocumentService.update_document(document_id, template_image, columns)
    if document:
        return jsonify({
            'id': document.id,
            'template_image': document.template_image,
            'columns': document.columns
        })
    return jsonify({'error': 'Document not found'}), 404


@document_bp.route('/documents/<document_id>', methods=['DELETE'])
def delete_document(document_id):
    document = DocumentService.delete_document(document_id)
    if document:
        return jsonify({'message': 'Document deleted successfully'})
    return jsonify({'error': 'Document not found'}), 404
