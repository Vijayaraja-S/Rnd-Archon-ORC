from flask import Blueprint

fields_bp = Blueprint('fields', __name__)


@fields_bp.route('/fields', methods=['GET', 'POST'])
def fields():
    pass
