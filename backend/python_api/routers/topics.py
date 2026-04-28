from fastapi import APIRouter, HTTPException, status, Depends
from typing import Sequence, Annotated, Literal
from sqlalchemy.orm import Session

from db.models import Topic
from db.session import get_session
from db.crud.topic import (
    get_all_topics, create_topic, delete_topic, get_topic_by_name
)
from python_api.auth import AuthRoute
from python_api.request_types import CreateTopicRequest, DeleteTopicRequest
from python_api.response_types import TopicResponse


unauthenticated_router = APIRouter()
authenticated_router = APIRouter(route_class=AuthRoute)


@authenticated_router.get('/topics', tags=["Topics"])
def topics(
    session: Annotated[Session, Depends(get_session)]
) -> Sequence[TopicResponse]:
    return list(map(
        lambda topic: TopicResponse(id=topic.id, name=topic.name),
        get_all_topics(session)
    ))


@authenticated_router.post('/create-topic', tags=["Topics"])
def create_topic_endpoint(
    request: CreateTopicRequest,
    session: Annotated[Session, Depends(get_session)]
) -> Literal["Topic created successfully"]:
    exists = get_topic_by_name(session, request.name)
    if exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=("Topic with given name already exists!")
        )
    create_topic(session, request.name)
    session.commit()
    return "Topic created successfully"


@authenticated_router.delete('/delete-topic', tags=["Topics"])
def delete_topic_endpoint(
    request: DeleteTopicRequest,
    session: Annotated[Session, Depends(get_session)]
) -> Literal["Topic has been successfully deleted"]:
    isDeleteSuccess = delete_topic(session, request.topic_id)
    session.commit()
    if isDeleteSuccess:
        return "Topic has been successfully deleted"
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=("Could not delete topic."
                    " Make sure it is not attached to any tasks.")
        )


topics_router = APIRouter()
topics_router.include_router(authenticated_router)
topics_router.include_router(unauthenticated_router)
