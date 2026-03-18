from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import List

from db.models import Topic


def get_all_topics(session: Session) -> List[Topic]:
    return session.query(Topic).all()


def create_topic(session: Session, name: str) -> Topic:
    topic = Topic(name=name)
    session.add(topic)
    return topic


def delete_topic(session: Session, topic_id: int) -> bool:
    topic = session.scalar(select(Topic).where(Topic.id == topic_id))
    if topic is None:
        return False
    if len(topic.tasks) != 0:
        return False
    session.delete(topic)
    return True
