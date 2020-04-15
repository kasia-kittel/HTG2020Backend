import datetime

from flask import Blueprint
from app.db import query_db, update_db

bp = Blueprint('badges', __name__, url_prefix='/badges')


# this suppose to run as a cron job but for now can be triggered from the url
# !! this is so low effort

@bp.route('/run/pioneer')
def run_pioneer():
    pioneers = assign_pioneer_badge();
    return pioneers


@bp.route('/run/hero')
def run_hero():
    heroes = assign_hero_badge();
    return heroes


@bp.route('/run/hero-of-the-week/<int:week>/<int:year>')
def run_hero_of_the_week(week, year):
    heroes = assign_hero_of_the_week(week, year)
    return heroes

# super pioneer badge - hardcoded


# pioneer badge
def assign_pioneer_badge():
    badge_name = "pioneer"
    badge_description = "One of the first 100 professionals with at least one confirmed appointment"

    pioneers = query_db('SELECT DISTINCT professional_id FROM appointments WHERE professional_scheduled is NOT NULL AND consumer_accepted is NOT NULL ORDER BY consumer_accepted asc', [])

    update_badge_table(badge_name, badge_description, pioneers)

    return pioneers


# hero badge
def assign_hero_badge():
    badge_name = "hero"
    badge_description = "Professional who spend more than 2 hours helping people in need."

    heroes = query_db('SELECT professional_id, SUM(appointment_duration) as total FROM appointments GROUP BY professional_id HAVING total >= 120', [])

    update_badge_table(badge_name, badge_description, heroes)

    return heroes


# hero of the week - most time spend on giving appointments in this week
def assign_hero_of_the_week(week, year):

    badge_name = f"hero of the week {week}"
    badge_description = "f10 professionals who spend most time helping people in need in week {week}/{year}."

    # libraries star counting weeks from 0 - this needs a bit more investigation
    c_week = week - 1
    week_start_date = datetime.datetime.strptime(f'{year}-{c_week}-1', "%Y-%W-%w").date()
    week_end_date = week_start_date + datetime.timedelta(days=7)

    heroes_of_the_week = query_db('SELECT professional_id, appointment_date, SUM(appointment_duration) as total FROM appointments WHERE appointment_date >=date(?) and appointment_date <= date(?) GROUP BY professional_id ORDER BY total DESC LIMIT 10',
                                   [week_start_date.isoformat(), week_end_date.isoformat()])

    update_badge_table(badge_name, badge_description, heroes_of_the_week)

    return heroes_of_the_week



def update_badge_table(badge_name, badge_description, professionals):

    #  update badge table
    for p in professionals:
        # update badge table
        update_db('INSERT INTO badges (badge_name, badge_description, professional_id) VALUES (?, ?, ?)',[badge_name, badge_description, p["professional_id"]])

        # update the search profile
        # this will add the same badge to the profile many time - this is ok for the beginning
        update_db('UPDATE profile_search SET profile = ? || \' \' || profile WHERE professional_id = ?', [badge_name, p["professional_id"]])
