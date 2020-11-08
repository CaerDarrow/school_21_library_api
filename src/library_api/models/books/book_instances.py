from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import func

from .. import db
from ..books.books import Books


class BookInstances(db.Model):
    __tablename__ = "book_instances"

    id = db.Column(UUID, primary_key=True, server_default=func.uuid_generate_v4(), nullable=False)
    book_id = db.Column(UUID, db.ForeignKey(Books.id), nullable=False)
    name = db.Column(db.Unicode(), default=None)
    desc = db.Column(db.Unicode(), default=None)
