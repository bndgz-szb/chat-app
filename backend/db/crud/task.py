from sqlalchemy.orm import Session
from db.models import Chat, Task, Topic, TaskTopic

def create_task(session: Session, name: str, chat: Chat) -> Task:
    task = Task(chat_id=chat.id, name=name, done=False)
    session.add(task)
    session.commit()
    return task

# if task already has topic attached, nothing happens
def attach_topic(session: Session, task: Task, topic: Topic) -> None:
    exists = session.query(TaskTopic).filter_by(task_id=task.id, topic_id=topic.id).first()
    if exists == None:
        taskTopic = TaskTopic(task_id=task.id, topic_id=topic.id)
        session.add(taskTopic)
        session.commit()
        session.refresh(task)
        session.refresh(topic)