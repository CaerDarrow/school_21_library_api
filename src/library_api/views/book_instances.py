import uuid
from fastapi import APIRouter, HTTPException, status, Query
from .base.base_api import BaseApiModel
from typing import List, Optional
from asyncpg.exceptions import ForeignKeyViolationError
from ..models.books.book_instances import BookInstances

router = APIRouter()


class BookInstanceModelIn(BaseApiModel):
    name: str


class BookInstanceModelOut(BaseApiModel):
    meta_id: uuid.UUID


class BookInstancesList(BaseApiModel):
    prev_page: Optional[str]
    next_page: Optional[str]
    instances: List[BookInstanceModelOut]


@router.get("/book/{uid}/instances", response_model=BookInstancesList)
async def get_book_instances(
        uid: uuid.UUID,
        skip: Optional[int] = Query(0, le=1000),
        limit: Optional[int] = Query(10, le=10),
):
    book_instances_list = await BookInstances.query.where(BookInstances.meta_id == uid).offset(skip).limit(limit).gino.all()
    if not book_instances_list:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No such data")
    cur_instances = BookInstancesList(**{'exemplars': book_instances_list})
    return cur_instances


@router.get("/book_instances/{uid}", response_model=BookInstanceModelOut)
async def get_book_instance(uid: uuid.UUID):
    book_instance = await BookInstances.get_or_404(uid)
    return book_instance


@router.post("/book_instances", response_model=BookInstanceModelOut)
async def add_book_instance(instance: BookInstanceModelIn):
    try:
        book_instance = await BookInstances.create(**instance.dict())
    except ForeignKeyViolationError:
        raise HTTPException(status.HTTP_409_CONFLICT, f"Haven't got meta with id {instance.dict().get('uid')}")
    return book_instance


def init_app(app):
    app.include_router(router)
