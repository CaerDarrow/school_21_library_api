from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import func

from .. import db


class BooksMeta(db.Model):
    __tablename__ = "books_meta"

    id = db.Column(UUID, primary_key=True, server_default=func.uuid_generate_v4())
    name = db.Column(db.Unicode(), default=None)
    desc = db.Column(db.Unicode(), default=None)
