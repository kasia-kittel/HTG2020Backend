from flask_api import status
from flask import Blueprint
from app.db import query_db, update_db

bp = Blueprint('consumers', __name__, url_prefix='/consumer')


@bp.route('/<int:id>')
def get_user(id):
    maybe_consumer = query_db('SELECT * FROM consumers WHERE id = ?', [id], one=True)

    if maybe_consumer is None:
        return {}, status.HTTP_404_NOT_FOUND
    else:
        return maybe_consumer


@bp.route('/<int:id>/bookmarks', methods=['GET'])
def get_bookmarks(id):
    maybe_bookmarks = query_db('SELECT professionals.id, fullname, qualifications, profession, specialties, languages '
                               'FROM professionals JOIN professionals_bookmarks ON (professionals.id = '
                               'professional_id) '
                               'WHERE professionals_bookmarks.consumer_id = ?', [id])

    if not maybe_bookmarks:
        return {}, status.HTTP_404_NOT_FOUND
    else:
        return maybe_bookmarks


@bp.route('/<int:id>/bookmark/<int:professional_id>', methods=['PUT'])
def update_bookmarks(id, professional_id):
    maybe_bookmark = query_db('SELECT professional_id FROM professionals_bookmarks WHERE consumer_id = ? AND  '
                              'professional_id = ? ', [id, professional_id])

    #  if bookmark exists remove it, else create it
    if not maybe_bookmark:
        r = update_db('INSERT INTO professionals_bookmarks (consumer_id, professional_id) values (?, ?)',
                 [id, professional_id])
        return {}, status.HTTP_202_ACCEPTED
    else:
        update_db('DELETE FROM professionals_bookmarks WHERE consumer_id = ? AND professional_id = ?',
                 [id, professional_id])
        return {}, status.HTTP_202_ACCEPTED
