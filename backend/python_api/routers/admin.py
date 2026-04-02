from fastapi import APIRouter, Depends
from typing import List, Annotated

from db.models import User
from db.session import SessionLocal
from db.crud.analytics import get_task_analytics, TaskWithAnalytics
from python_api.auth import AuthRoute, credentials_exception, get_current_user


admin_router = APIRouter(route_class=AuthRoute)


@admin_router.get('/analytics')
def get_analytics(
    user: Annotated[User | None, Depends(get_current_user)]
) -> List[TaskWithAnalytics]:
    if user is None or not user.admin:
        raise credentials_exception()
    with SessionLocal() as session:
        return get_task_analytics(session)
