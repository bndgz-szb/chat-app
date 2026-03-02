from sqlalchemy.orm import Session
from typing import List
from db.models import Topic


def create_topic(session: Session, name: str) -> Topic:
    topic = Topic(name=name)
    session.add(topic)
    session.commit()
    return topic


def get_all_topics(session: Session) -> List[Topic]:
    return session.query(Topic).all()
