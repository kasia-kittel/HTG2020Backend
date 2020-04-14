import sys

from flask_api import status
from flask import Blueprint, request
from app.db import query_db, update_db

bp = Blueprint('appointments', __name__, url_prefix='/appointments')


# there is no sessions or authorisation mechanism
# for convenience the user id that should be read from session is always in the end of the url

# --- consumer
@bp.route('/request-availability/<int:pid>/<int:cid>', methods=['PUT'])
def request_availability(pid, cid):
    id = update_db('INSERT INTO appointments (professional_id, consumer_id) values (?, ?)', [pid, cid])

    return {"id": id}, status.HTTP_201_CREATED


@bp.route('/accept-availability/<int:aid>/<int:pid>/<int:cid>', methods=['PUT'])
def accept_availability(aid, pid, cid):
    update_db('UPDATE appointments SET consumer_accepted = CURRENT_TIMESTAMP WHERE professional_id = ? AND '
              'consumer_id = ? AND id = ?', [pid, cid, aid])

    return {}, status.HTTP_202_ACCEPTED


@bp.route('/reject-availability/<int:aid>/<int:pid>/<int:cid>', methods=['PUT'])
def resign_availability(aid, pid, cid):
    update_db('UPDATE appointments SET consumer_resigned = CURRENT_TIMESTAMP WHERE professional_id = ? AND '
              'consumer_id = ? AND id = ?', [pid, cid, aid])

    return {}, status.HTTP_202_ACCEPTED


# requested by the consumer but not scheduled/rejected by the professional
@bp.route('/list-requested/<int:cid>', methods=['GET'])
def list_requested(cid):
    maybe_requests = query_db(
        'SELECT appointments.id, professional_id, requested, professionals.fullname, professionals.qualifications, professionals.profession FROM appointments JOIN professionals ON ('
        'professionals.id = professional_id) WHERE professional_declined is NULL AND professional_scheduled '
        'is NULL AND consumer_id =?', [cid])

    if not maybe_requests:
        return {}, status.HTTP_404_NOT_FOUND
    else:
        return maybe_requests


# requested by the consumer and scheduled by the professional
@bp.route('/list-requested-scheduled/<int:cid>', methods=['GET'])
def list_requested_scheduled(cid):
    maybe_requests = query_db(
        'SELECT appointments.id AS appointments_id, professional_id, requested, professionals.fullname, professionals.qualifications, professionals.profession, professional_scheduled, appointment_date, appointment_duration FROM appointments JOIN professionals ON ('
        'professionals.id = professional_id) WHERE professional_declined is NULL AND professional_scheduled '
        'is NOT NULL AND consumer_id =?', [cid])

    if not maybe_requests:
        return {}, status.HTTP_404_NOT_FOUND
    else:
        return maybe_requests


# requested by the consumer and declined by the professional
@bp.route('/list-requested-declined/<int:cid>', methods=['GET'])
def list_requested_declined(cid):
    maybe_requests = query_db(
        'SELECT appointments.id AS appointments_id, professional_id, requested, professionals.fullname, professionals.qualifications, professionals.profession, professional_declined FROM appointments JOIN professionals ON ('
        'professionals.id = professional_id) WHERE professional_declined is NOT NULL AND professional_scheduled '
        'is NULL AND consumer_id =?', [cid])

    if not maybe_requests:
        return {}, status.HTTP_404_NOT_FOUND
    else:
        return maybe_requests


# --- professional
@bp.route('/decline-availability-requests/<int:aid>/<int:pid>', methods=['PUT'])
def decline_availability_requests(aid, pid):
    update_db('UPDATE appointments SET professional_declined = CURRENT_TIMESTAMP WHERE professional_id = ? AND id = ?', [pid,aid])

    return {}, status.HTTP_202_ACCEPTED


@bp.route('/accept-availability-requests/<int:aid>/<int:pid>', methods=['POST'])
def accept_availability_requests(aid, pid):
    # front-end needs to convert it to UTC ie. 2020-05-01 11:00:00
    appointment_date_time = request.form['date-time']
    appointment_duration_min = request.form['duration-min']

    update_db('UPDATE appointments SET professional_scheduled = CURRENT_TIMESTAMP, appointment_date = ?, '
              'appointment_duration = ? WHERE professional_id = ? AND id = ?', [appointment_date_time, appointment_duration_min, pid,aid])

    return {}, status.HTTP_202_ACCEPTED

# list availability requests (not scheduled or declined)
@bp.route('/list-availability-requests/<int:pid>', methods=['GET'])
def list_availability_requests(pid):
    maybe_requests = query_db(
        'SELECT appointments.id AS appointments_id, consumer_id, consumers.username, requested FROM appointments JOIN '
        'consumers ON ( consumers.id = consumer_id) WHERE professional_declined is NULL AND professional_scheduled '
        'is NULL AND professional_id =?', [pid])

    if not maybe_requests:
        return {}, status.HTTP_404_NOT_FOUND
    else:
        return maybe_requests


@bp.route('/list-appointments-scheduled-and-confirmed/<int:pid>', methods=['GET'])
def list_availability_requests_scheduled(pid):
    maybe_requests = query_db(
        'SELECT appointments.id AS appointments_id, consumer_id, professional_id, consumers.username, requested, '
        'professional_scheduled, appointment_date, appointment_duration, consumer_accepted FROM appointments JOIN '
        'consumers ON (consumers.id = consumer_id) WHERE professional_declined is NULL AND professional_scheduled is '
        'NOT NULL AND consumer_accepted is NOT NULL AND professional_id =?', [pid])

    if not maybe_requests:
        return {}, status.HTTP_404_NOT_FOUND
    else:
        return maybe_requests


@bp.route('/list-appointments-scheduled-and-rejected/<int:pid>', methods=['GET'])
def list_availability_requests_declined(pid):
    maybe_requests = query_db(
        'SELECT appointments.id AS appointments_id, consumer_id, professional_id, consumers.username, requested, consumer_resigned FROM appointments JOIN consumers ON ('
        'consumers.id = consumer_id) WHERE professional_declined is NULL AND professional_scheduled '
        'is NOT NULL AND consumer_resigned is NOT NULL AND professional_id =?', [pid])

    if not maybe_requests:
        return {}, status.HTTP_404_NOT_FOUND
    else:
        return maybe_requests

