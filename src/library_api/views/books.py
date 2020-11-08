import uuid
from fastapi import APIRouter, HTTPException, status
from asyncpg.exceptions import UniqueViolationError
from sqlalchemy.dialects.postgresql import insert
from .base.base_api import BaseApiModel
from typing import List
from ..models import db
from ..models.books.books import Books
from ..models.tags.tags import Tags, TagsAliases, TagsAliasesBooks

router = APIRouter()


class TagsAliasIn(BaseApiModel):
    name: str


class TagsAliasOut(TagsAliasIn):
    id: uuid.UUID
    normalized_name: str


class BookModelIn(BaseApiModel):
    name: str
    desc: str
    authors: str
    edition_number: int
    edition_year: int
    buy_url: str
    cover_url: str
    tags: List[TagsAliasIn]


class BookModelOut(BookModelIn):
    id: uuid.UUID
    tags: List[TagsAliasOut]


class BookModelList(BaseApiModel):
    books: List[BookModelOut]


@router.get("/books", response_model=BookModelList)
async def get_books():
    books = await Books.get_or_404()
    return books


@router.get("/books/{uid}", response_model=BookModelOut)
async def get_book(uid: uuid.UUID):
    query = Books.outerjoin(TagsAliasesBooks).outerjoin(TagsAliases).select().where(Books.id == uid)
    book = await query.gino.load(Books.distinct(Books.id).load(tags=TagsAliases.distinct(TagsAliases.id))).first()
    # book = await Books.get_or_404(uid)
    return book


@router.patch("/books/{uid}", response_model=BookModelOut)
async def update_book(uid: uuid.UUID, book: BookModelIn):
    book_record = await Books.get_or_404(id=uid)
    await book_record.update(**book.dict(exclude={'tags'})).apply()
    return book_record


@router.post("/books", response_model=BookModelOut)
async def add_book(book: BookModelIn):
    async with db.transaction() as tx:
        try:
            new_book = await Books.create(**book.dict(exclude={'tags'}))
        except Exception as e:
            raise HTTPException(status.HTTP_409_CONFLICT, f"{e}")
        tags = book.dict(include={'tags'}).get('tags', {})
        for tag in tags:
            try:
                normalized_name = 'loh2'  # tag.get('name').strip()
                new_tag = await insert(Tags).values(name=normalized_name).on_conflict_do_nothing().gino.model(Tags).first()
                tag |= {'normalized_name': normalized_name}
                print(tag)
                new_tag_alias = await TagsAliases.create(**tag)
                new_book.tags = new_tag_alias
                await TagsAliasesBooks.create(**{"tag": new_tag_alias.id, "book": new_book.id})
            except UniqueViolationError as e:
                raise HTTPException(status.HTTP_409_CONFLICT, f"{e}")
    return new_book


@router.delete("/books/{uid}")
async def delete_book(uid: int):
    book = await Books.get_or_404(uid)
    await book.delete()
    return dict(id=uid)


def init_app(app):
    app.include_router(router)
