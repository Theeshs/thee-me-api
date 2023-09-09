""" service controllers for the educations """
from sqlalchemy.orm import Session
from thee_me.handlers.


def get_all_educations(db: Session, user_id: int):
    return list_educations(db, user_id)