from ..services.document_service import DocumentService
from flask import Blueprint, request, jsonify

from ..models.beans import ImageDetails

document_bp = Blueprint('document', __name__)


@document_bp.route('/documents/<document_type_id>', methods=['POST'])
def create_document(document_type_id):
    data = request.json
    if not data:
        return jsonify({'error': 'Template image is required'}), 400

    document = DocumentService.save_document(ImageDetails(**data), document_type_id)
    return jsonify({
        'id': document.id,
        "message": "Document created",
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


@document_bp.route('/documents/<document_id>', methods=['DELETE'])
def delete_document(document_id):
    document = DocumentService.delete_document(document_id)
    if document:
        return jsonify({'message': 'Document deleted successfully'})
    return jsonify({'error': 'Document not found'}), 404
