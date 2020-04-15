from builtins import len
from re import sub
from flask_api import status
from flask import (Blueprint, request, current_app)
from app.db import query_db

app = current_app

bp = Blueprint('professionals', __name__, url_prefix='/professional')


@bp.route('/<int:id>')
def get_user(id):
    maybe_professionals = query_db('SELECT * FROM professionals WHERE id = ?', [id], one=True)

    if maybe_professionals is None:
        return {}, status.HTTP_404_NOT_FOUND
    else:
        maybe_badges = query_db('SELECT * FROM badges WHERE professional_id = ?', [id])
        maybe_professionals["badges"] = maybe_badges
        return maybe_professionals


@bp.route('/search', methods=['POST'])
def search():
    # payload expected as x-www-form-urlencoded
    # accepts a list of words separated with whitespaces, commas etc
    # takes into consideration only 5 first words
    # two first words are most important
    # not-secure for demo only
    criteria = create_criteria_list(request.form['s'])
    term = create_matching_term(criteria)
    matching_profiles = query_db('SELECT DISTINCT professional_id, fullname, qualifications, profession '
                                 'FROM profile_search WHERE profile MATCH ? ORDER BY rank', [term])

    return matching_profiles


def create_criteria_list(raw):
    # clean semicolons and commas
    s1 = sub("[,;+]", " ", raw)

    # clean white spaces
    s2 = sub(" +", " ", s1.strip())

    return s2.split(" ")[:5]


def create_matching_term(criteria_list):
    # should I test if the criteria_list is really of type list?
    first_part = " ".join(criteria_list[:2])
    if len(criteria_list) > 2:
        second_part = " OR ".join(criteria_list[2:])
        return first_part + " AND (" + second_part + ")"

    return first_part
