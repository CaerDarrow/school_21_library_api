import uuid
from fastapi import APIRouter, HTTPException, status, Query
from pydantic import BaseModel
from typing import List, Optional
from asyncpg.exceptions import ForeignKeyViolationError
from ..models.books.book_exemplars import BooksExemplars

router = APIRouter()


class BookExemplarModelIn(BaseModel):
    meta_id: uuid.UUID
    name: str
    desc: str

    class Config:
        orm_mode = True


class BookExemplarModelOut(BaseModel):
    meta_id: uuid.UUID
    name: str
    desc: str

    class Config:
        orm_mode = True


@router.get("/books/{uid}/exemplars", response_model=List[BookExemplarModelOut])
async def get_book_exemplars(
        uid: uuid.UUID,
        skip: Optional[int] = Query(0, le=1000),
        limit: Optional[int] = Query(10, le=10),
):
    books_exemplars_list = await BooksExemplars.query.where(BooksExemplars.meta_id == uid).offset(skip).limit(limit).gino.all()
    if not books_exemplars_list:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No such data")
    return books_exemplars_list


@router.get("/exemplars/{uid}", response_model=BookExemplarModelOut)
async def get_book_exemplar(uid: uuid.UUID):
    rv = await BooksExemplars.get_or_404(uid)
    return rv


@router.post("/exemplars", response_model=BookExemplarModelOut)
async def add_book_exemplar(exemplar: BookExemplarModelIn):
    try:
        rv = await BooksExemplars.create(**exemplar.dict())
    except ForeignKeyViolationError:
        raise HTTPException(status.HTTP_409_CONFLICT, f"Haven't got meta with id {exemplar.dict().get('uid')}")
    return rv


def init_app(app):
    app.include_router(router)
