import random
from faker import Faker
from sqlalchemy.orm import Session
from sqlalchemy import delete
from typing import List, Tuple, Dict
from db.session import SessionLocal
from db.models import *
from python_api.auth import get_password_hash
from db.crud import (
    create_user, create_chat, create_task, create_topic, attach_topic,
    assign_user, send_message_to_chat, ChatRole
)


def seed():
    with SessionLocal() as session:
        delete_records(session)
        fake = Faker()

        users = generate_users(session, fake, 10)
        tasks, chats = generate_tasks_and_chats(session, fake, users, 10)
        topics = generate_topics(session, fake, 11)
        generate_task_topic_relations(session, tasks, topics)
        chat_to_list_of_users = generate_chat_user_relations(
            session, users, chats
        )
        generate_messages(session, fake, chat_to_list_of_users)
        generate_admin(session, tasks)


def generate_users(
        session: Session, fake: Faker, number_of_users: int
) -> List[User]:
    users = [
        create_user(
            username=fake.unique.user_name(),
            hashed_password=get_password_hash('password'),
            email=fake.unique.email(),
            session=session
        )
        for _ in range(number_of_users)
    ]
    session.commit()
    return users


def generate_tasks_and_chats(
        session: Session, fake: Faker, users: List[User], number_of_tasks: int
) -> Tuple[List[Task], List[Chat]]:
    chats = [create_chat(session) for _ in range(number_of_tasks)]
    session.commit()
    tasks = [
        create_task(
            session=session,
            name=fake.unique.city(),
            chat=chat,
            creator=random.choice(users)
        )
        for chat in chats
    ]
    session.commit()
    for task in tasks:
        assign_user(session, task.chat.id, task.creator.id, ChatRole.OWNER)
    session.commit()
    return tasks, chats


def generate_topics(
        session: Session, fake: Faker, number_of_topics: int
) -> List[Topic]:
    topics = [
        create_topic(session, fake.unique.safe_color_name())
        for _ in range(number_of_topics)
    ]
    session.commit()
    return topics


def generate_task_topic_relations(
        session: Session, tasks: List[Task], topics: List[Topic]
) -> None:
    for task in tasks:
        selected_topics = random.sample(
            population=topics, k=random.randint(1, 4)
        )
        for topic in selected_topics:
            attach_topic(session, task, topic.id)
    session.commit()


def generate_chat_user_relations(
        session: Session, users: List[User], chats: List[Chat]
) -> Dict[Chat, List[User]]:
    res = dict()
    for chat in chats:
        res[chat] = []
        selected_users = random.sample(
            population=users, k=random.randint(2, 4)
        )
        for user in selected_users:
            assign_user(session, chat.id, user.id)
            res[chat].append(user)
    session.commit()
    return res


def generate_messages(
        session: Session, fake: Faker,
        chat_to_list_of_users: Dict[Chat, List[User]]
) -> None:
    for chat in chat_to_list_of_users.keys():
        for user in chat_to_list_of_users[chat]:
            for _ in range(random.randint(0, 10)):
                send_message_to_chat(
                    session, chat, user, fake.text(max_nb_chars=200),
                    fake.date_time_between(start_date='-1w')
                    .strftime('%Y-%m-%d %H:%M:%S.%f')
                )
    session.commit()


def generate_admin(session: Session, tasks: List[Task]):
    admin = User(username='admin', password=get_password_hash(
        'admin'), email='admin@example.com', admin=True
    )
    session.add(admin)
    session.commit()
    for task in tasks:
        assign_user(session, task.chat.id, admin.id, ChatRole.OWNER)
    session.commit()


def delete_records(session: Session):
    session.execute(delete(Message))
    session.execute(delete(ChatParticipant))
    session.execute(delete(TaskTopic))
    session.execute(delete(Topic))
    session.execute(delete(Task))
    session.execute(delete(Chat))
    session.execute(delete(User))
    session.commit()


seed()
