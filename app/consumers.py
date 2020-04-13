from flask_api import status
from flask import Blueprint
from app.db import query_db

bp = Blueprint('consumers', __name__, url_prefix='/consumer')


@bp.route('/<int:id>')
def get_user(id):

    maybe_consumer = query_db('SELECT * FROM consumers WHERE id = ?', [id], one=True)

    if maybe_consumer is None:
        return {}, status.HTTP_404_NOT_FOUND
    else:
        return maybe_consumer


