from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import func

from .. import db
from..books.books import Books


class Tags(db.Model):
    __tablename__ = "tags"

    name = db.Column(db.Unicode(), primary_key=True, nullable=False)


class TagsAliases(db.Model):
    __tablename__ = "tags_aliases"

    id = db.Column(UUID, primary_key=True, server_default=func.uuid_generate_v4())
    name = db.Column(db.Unicode(), default=None)
    normalized_name = db.Column(db.Unicode(), db.ForeignKey(Tags.name), nullable=False)


class TagsAliasesBooks(db.Model):
    __tablename__ = "tags_aliases_books"

    tag = db.Column(UUID, db.ForeignKey(TagsAliases.id), nullable=False)
    book = db.Column(UUID, db.ForeignKey(Books.id), nullable=False)
