from fastapi import APIRouter, HTTPException, status
from typing import Sequence

from db.models import Topic
from db.session import SessionLocal
from db.crud.topic import get_all_topics, create_topic, delete_topic
from python_api.auth import AuthRoute
from python_api.request_types import CreateTopicRequest, DeleteTopicRequest


unauthenticated_router = APIRouter()
authenticated_router = APIRouter(route_class=AuthRoute)


@authenticated_router.get('/topics', response_model=None)
def topics() -> Sequence[Topic]:
    with SessionLocal() as session:
        return get_all_topics(session)


@authenticated_router.post('/create-topic')
def create_topic_endpoint(request: CreateTopicRequest) -> str:
    with SessionLocal.begin() as session:
        create_topic(session, request.name)
    return "Topic created successfully"


@authenticated_router.delete('/delete-topic')
def delete_topic_endpoint(request: DeleteTopicRequest) -> str:
    with SessionLocal.begin() as session:
        isDeleteSuccess = delete_topic(session, request.topic_id)
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
