import uuid
from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Query
from .base.base_api import BaseApiModel
from typing import List, Optional
from asyncpg.exceptions import ForeignKeyViolationError
from pydantic import validator
from ..models.books.book_instance_states import BookInstanceStates

router = APIRouter()


class BookInstanceStateModelIn(BaseApiModel):
    instance_id: uuid.UUID
    user: Optional[uuid.UUID]
    cluster: Optional[uuid.UUID]

    @validator('user')
    def only_user(cls, v, values, **kwargs):
        assert values.get('user'), "must specify either user or cluster"
        assert not values.get('cluster'), "can't specify both user and cluster"
        return v

    @validator('cluster')
    def only_cluster(cls, v, values, **kwargs):
        assert values.get('cluster'), "must specify either user or cluster"
        assert not values.get('user'), "can't specify both user and cluster"
        return v


class BookInstanceStateModelOut(BookInstanceStateModelIn):
    id: uuid.UUID
    action_date: datetime


class BookInstanceStatesList(BaseApiModel):
    prev_page: Optional[str] = None
    next_page: Optional[str]
    states: List[BookInstanceStateModelOut]


@router.get("/book_instance/{uid}/states", response_model=BookInstanceStatesList)
async def get_book_instance_states(
        uid: uuid.UUID,
        skip: Optional[int] = Query(0, le=1000),
        limit: Optional[int] = Query(10, le=10),
):
    book_instance_states_list = await BookInstanceStates.query.where(
        BookInstanceStates.instance_id == uid
    ).order_by(
        BookInstanceStates.action_date.desc()
    ).offset(skip).limit(limit).gino.all()
    if not book_instance_states_list:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No such data")
    cur_states = BookInstanceStatesList(**{'states': book_instance_states_list})
    return cur_states


@router.post("/book_instance_states", response_model=BookInstanceStateModelOut)
async def add_book_book_instance_state(state: BookInstanceStateModelIn):
    try:
        book_instance_state = await BookInstanceStates.create(**state.dict())
    except ForeignKeyViolationError:
        raise HTTPException(status.HTTP_409_CONFLICT, f"Haven't got instance with id {state.dict().get('uid')}")
    return book_instance_state

# @router.get("/book_instances/{uid}", response_model=BookInstanceModelOut)
# async def get_book_exemplar(uid: uuid.UUID):
#     rv = await BookInstances.get_or_404(uid)
#     return rv


def init_app(app):
    app.include_router(router)
