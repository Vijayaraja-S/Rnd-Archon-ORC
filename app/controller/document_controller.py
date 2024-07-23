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
    response_bean = DocumentService.get_document_response(document_id)

    if response_bean.document_info:
        return jsonify(response_bean.dict())

    return jsonify(response_bean.dict())



    # results, fields, document = DocumentService.get_document(document_id)
    # results_response = [ResultsInfoResponse(id=UUID(result.id), value=result.value) for result in results]
    #
    # field_id_map = {field.id: field for field in fields}
    #
    # fields_response = []
    # for result in results:
    #     field = field_id_map.get(result.field_id)
    #     if field:
    #         if isinstance(field.coordinates, str):
    #             try:
    #                 coordinates = json.loads(field.coordinates)
    #             except json.JSONDecodeError:
    #                 coordinates = {}
    #         else:
    #             coordinates = field.coordinates or {}
    #
    #         fields_response.append(
    #             FieldInfo(
    #                 bindingName=field.binding_name,
    #                 position=Position(
    #                     x=coordinates.get('x', 0),  # Default to 0 if not present
    #                     y=coordinates.get('y', 0),
    #                     width=coordinates.get('width', 0),
    #                     height=coordinates.get('height', 0)
    #                 ),
    #                 value=result.value,
    #                 #accuracy=field.accuracy
    #             )
    #         )
    #
    # if document:
    #     document_response = DocumentInfo(
    #         id=document.id,
    #         image_name=document.image_name,
    #         image_content=document.image_content,
    #         createdAt=document.created_date.isoformat(),
    #         modifiedAt=document.modified_date.isoformat() if document.modified_date else None,
    #         status=document.status
    #     )
    #
    #     response_bean = DocumentResponseBean(
    #         document_info=[document_response],
    #         document_type_id=document.document_type_id,
    #         fields=fields_response,
    #         results=results_response
    #     )
    #
    #     return jsonify(response_bean.dict())
    #
    # return jsonify({'error': 'Document not found'}), 404


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
