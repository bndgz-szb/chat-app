from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import List

from db import models

def get_chats_for_user(session: Session, user_id: int) -> List[str]:
	stmt = (
		select(models.Chat.name)
		.join(models.ChatParticipant)
		.where(models.ChatParticipant.user_id == user_id)
	)
	result = session.execute(stmt).scalars().all()
	return result
