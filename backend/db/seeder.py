import random
from faker import Faker
from sqlalchemy.orm import Session
from typing import List, Tuple, Dict
from db.session import SessionLocal
from db.models import User, Chat, Task, Topic, TaskTopic
from python_api.auth import get_password_hash
from db.crud import (
    create_user, create_chat, create_task, create_topic, attach_topic,
    assign_user, send_message_to_chat
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


def generate_users(
        session: Session, fake: Faker, number_of_users: int
) -> List[User]:
    admin = User(username='admin', password=get_password_hash(
        'admin'), email='admin@example.com', admin=True
    )
    session.add(admin)
    session.commit()
    session.refresh(admin)
    users = []
    for _ in range(number_of_users):
        user = create_user(
            username=fake.user_name(),
            hashed_password=get_password_hash('password'),
            email=fake.email(),
            session=session
        )
        users.append(user)
    return users


def generate_tasks_and_chats(
        session: Session, fake: Faker, users: List[User], number_of_tasks: int
) -> Tuple[List[Task], List[Chat]]:
    chats, tasks = [], []
    for _ in range(number_of_tasks):
        task_creator = random.choice(users)
        chat = create_chat(session)
        task = create_task(session, fake.city(), chat, task_creator)
        chats.append(chat)
        tasks.append(task)
    return tasks, chats


def generate_topics(
        session: Session, fake: Faker, number_of_topics
) -> List[Topic]:
    topics = []
    for _ in range(number_of_topics):
        topic = create_topic(session, fake.safe_color_name())
        topics.append(topic)
    return topics


def generate_task_topic_relations(
        session: Session, tasks: List[Task], topics: List[Topic]
) -> None:
    for task in tasks:
        selected_topics = random.choices(
            population=topics, k=random.randint(1, 4)
        )
        for topic in selected_topics:
            attach_topic(session, task, topic)


def generate_chat_user_relations(
        session: Session, users: List[User], chats: List[Chat]
) -> Dict[Chat, List[User]]:
    res = dict()
    for chat in chats:
        res[chat] = []
        selected_users = random.choices(
            population=users, k=random.randint(2, 4)
        )
        for user in selected_users:
            assign_user(session, chat, user)
            res[chat].append(user)
    return res


def generate_messages(
        session: Session, fake: Faker,
        chat_to_list_of_users: Dict[Chat, List[User]]
) -> None:
    for chat in chat_to_list_of_users.keys():
        for user in chat_to_list_of_users[chat]:
            for _ in range(random.randint(0, 10)):
                # TODO randomize 'sent_at' parameter as well
                send_message_to_chat(
                    session, chat, user,
                    fake.text(max_nb_chars=200)
                )


def delete_records(session: Session):
    session.query(TaskTopic).delete()
    session.query(Topic).delete()
    session.query(Task).delete()
    session.query(Chat).delete()
    session.query(User).delete()
    session.commit()


seed()
