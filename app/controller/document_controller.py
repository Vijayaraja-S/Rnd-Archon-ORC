from flask import Blueprint, request, jsonify

from ..model.beans.request_bean import DocumentRequestBean
from ..service.document_service import DocumentService

document_bp = Blueprint('document', __name__)


@document_bp.route('/documents/<document_type_id>', methods=['POST'])
def create_document(document_type_id):
    data = request.json
    if not data:
        return jsonify({'error': 'Template image is required'}), 400

    document = DocumentService.save_document_info(DocumentRequestBean(**data), document_type_id)
    return jsonify({
        'id': document.id,
        "message": "Document created",
    }), 201


@document_bp.route('/documents/<document_id>', methods=['GET'])
def get_document(document_id):
    document = DocumentService.get_document(document_id)
    print("document", document)
    if document:
        return jsonify({
            'id': document.id,
            'image_content': document.image_content,
            'image_name': document.image_name,
            'created_date': document.created_date,
            'modified_date': document.modified_date,
            'document_type_id': document_id

        })
    return jsonify({'error': 'Document not found'}), 404


@document_bp.route('/list_documents', methods=['GET'])
def list_documents():
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        image_name = request.args.get('image_name', None)
        status = request.args.get('status', None)

        result = DocumentService.get_all_documents(page, per_page, image_name, status)

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@document_bp.route('/documents/<document_id>', methods=['DELETE'])
def delete_document(document_id):
    document = DocumentService.delete_document(document_id)
    if document:
        return jsonify({'message': 'Document deleted successfully'})
    return jsonify({'error': 'Document not found'}), 404


@document_bp.route('/check_document_exists', methods=['GET'])
def check_document_exists():
    image_name = request.args.get('image_name')
    if not image_name:
        return jsonify({'error': 'Image name is required'}), 400

    exists = DocumentService.check_document_exists(image_name) is not None
    return jsonify({'exists': exists}), 200
