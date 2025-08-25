from sqlalchemy.orm import Session

from db.models import User

def get_user_by_username(session: Session, username: str) -> User:
	return session.query(User).filter_by(username=username).first()

def create_user(session: Session, username: str, hashed_password: str) -> User:
	user = User(username=username, password=hashed_password)
	session.add(user)
	session.commit()
	session.refresh(user)
	return user