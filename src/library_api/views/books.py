import uuid
from fastapi import APIRouter
from pydantic import BaseModel

from ..models.books.book_meta import BooksMeta
from ..models.books.book_exemplars import BooksExemplars

router = APIRouter()


class BookModel(BaseModel):
    name: str


@router.get("/books/{uid}")
async def get_book(uid: uuid.UUID):
    user = await BooksMeta.get_or_404(uid)
    return user.to_dict()


@router.get("/books/{uid}/exemplars")
async def get_book(uid: uuid.UUID):
    user = await BooksExemplars.get_or_404(uid)
    return user.to_dict()


@router.post("/books")
async def add_book(book: BookModel):
    rv = await BooksMeta.create(name=book.name)
    return rv.to_dict()


@router.delete("/books/{uid}")
async def delete_book(uid: int):
    user = await BooksMeta.get_or_404(uid)
    await user.delete()
    return dict(id=uid)


def init_app(app):
    app.include_router(router)
