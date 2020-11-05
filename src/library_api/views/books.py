import uuid
from fastapi import APIRouter
from pydantic import BaseModel
from ..models.books.book_meta import BooksMeta


router = APIRouter()


class BookMetaModelIn(BaseModel):
    name: str

    class Config:
        orm_mode = True


class BookMetaModelOut(BaseModel):
    id: uuid.UUID
    name: str

    class Config:
        orm_mode = True


@router.get("/books/{uid}", response_model=BookMetaModelOut)
async def get_book(uid: uuid.UUID):
    book_meta = await BooksMeta.get_or_404(uid)
    return book_meta


@router.post("/books", response_model=BookMetaModelOut)
async def add_book(book: BookMetaModelIn):
    book_meta = await BooksMeta.create(name=book.name)
    return book_meta


@router.delete("/books/{uid}")
async def delete_book(uid: int):
    user = await BooksMeta.get_or_404(uid)
    await user.delete()
    return dict(id=uid)


def init_app(app):
    app.include_router(router)
