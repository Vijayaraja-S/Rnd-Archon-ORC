from flask import Blueprint


document_bp = Blueprint('document', __name__)
document_type_bp = Blueprint('document_type', __name__)

from . import document_controller, document_type_controller
