from flask_api import status
from flask import Blueprint
from app.db import query_db

bp = Blueprint('professionals', __name__, url_prefix='/professional')


@bp.route('/<int:id>')
def get_user(id):

    maybe_consumer = query_db('SELECT * FROM professionals WHERE id = ?', [id], one=True)

    if maybe_consumer is None:
        return {}, status.HTTP_404_NOT_FOUND
    else:
        return maybe_consumer


