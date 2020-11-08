import uuid

from fastapi import APIRouter
from .base.base_api import BaseApiModel
from typing import List
from ..models.books.books import Books

router = APIRouter()


class BookModelIn(BaseApiModel):
    name: str
    desc: str
    authors: List[str]
    edition_number: int
    edition_year: int
    buy_url: str
    cover_url: str


class BookModelOut(BookModelIn):
    id: uuid.UUID


class BookModelList(BaseApiModel):
    books: List[BookModelOut]


@router.get("/books", response_model=BookModelList)
async def get_books():
    books = await Books.get_or_404()
    return books


@router.get("/books/{uid}", response_model=BookModelOut)
async def get_book(uid: uuid.UUID):
    book = await Books.get_or_404(uid)
    return book


@router.patch("/books/{uid}", response_model=BookModelOut)
async def update_book(book: BookModelIn):
    book = await Books.create(name=book.name)
    return book


@router.post("/books", response_model=BookModelOut)
async def add_book(book: BookModelIn):
    book = await Books.create(name=book.name)
    return book


@router.delete("/books/{uid}")
async def delete_book(uid: int):
    book = await Books.get_or_404(uid)
    await book.delete()
    return dict(id=uid)


def init_app(app):
    app.include_router(router)
