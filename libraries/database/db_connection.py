import datetime
from .db import get_database_session
from model import Member


def create_member(user_id, name, desc, points, status):
    session = get_database_session()
    new_member = Member(user_id, name, desc, points, datetime.datetime.now(), status)
    session.add(new_member)
    session.commit()
    session.close()


def update_member(user_id: int = None, status: str = None, bot_start: bool = False, gamble_points: int = 0):
    session = get_database_session()
    now = datetime.datetime.now()
    member = session.query(Member).filter(Member.id == user_id).one()
    points = 0
    if not bot_start:
        if member.status != "offline":
            delta = (datetime.datetime.now() - member.update_time).total_seconds()
            points += int(delta / 10)
            session.query(Member).filter(Member.id == user_id).update({Member.points: Member.points + points})
        if gamble_points:
            points += gamble_points
            session.query(Member).filter(Member.id == user_id).update({Member.points: Member.points + points})
    session.query(Member).filter(Member.id == user_id).update({Member.update_time: now})
    session.query(Member).filter(Member.id == user_id).update({Member.status: status})
    session.commit()


def get_all_members():
    session = get_database_session()
    people_query = session.query(Member)
    session.close()
    return people_query.all()


def get_member(user_id: int = None):
    session = get_database_session()
    people_query = session.query(Member).filter(Member.id == user_id)
    session.close()
    return people_query.one()
