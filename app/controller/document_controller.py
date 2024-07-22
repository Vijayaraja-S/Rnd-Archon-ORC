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


@document_bp.route('/documents', methods=['GET'])
def list_documents():
    documents = DocumentService.get_all_documents()

    if not documents:
        return jsonify({'message': 'No documents found'}), 404

    response = [{
        'id': doc.id,
        'image_content': doc.image_content,
        'image_name': doc.image_name,
        'created_date': doc.created_date,
        'modified_date': doc.modified_date,
        'document_type_id': doc.document_type_id
    } for doc in documents]

    return jsonify(response)



@document_bp.route('/documents/<document_id>', methods=['DELETE'])
def delete_document(document_id):
    document = DocumentService.delete_document(document_id)
    if document:
        return jsonify({'message': 'Document deleted successfully'})
    return jsonify({'error': 'Document not found'}), 404
