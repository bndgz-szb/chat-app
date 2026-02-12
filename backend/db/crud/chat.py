from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import List

from db.models import Chat, ChatParticipant

def get_chats_for_user(session: Session, user_id: int) -> List[str]:
	stmt = (
		select(Chat.id)
		.join(ChatParticipant)
		.where(ChatParticipant.user_id == user_id)
	)
	result = session.execute(stmt).scalars().all()
	return result
