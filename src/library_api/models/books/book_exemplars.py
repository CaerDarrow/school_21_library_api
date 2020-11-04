from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import func

from .. import db


class BooksExemplars(db.Model):
    __tablename__ = "books_exemplars"

    id = db.Column(UUID, primary_key=True, server_default=func.uuid_generate_v4())
    meta_id = db.Column(UUID, db.ForeignKey("books_meta.id"))
    name = db.Column(db.Unicode(), default=None)
    desc = db.Column(db.Unicode(), default=None)
