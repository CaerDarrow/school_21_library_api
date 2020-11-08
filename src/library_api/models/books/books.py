from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import func

from .. import db


class Books(db.Model):
    __tablename__ = "books"

    id = db.Column(UUID, primary_key=True, server_default=func.uuid_generate_v4(), nullable=False)
    name = db.Column(db.Unicode(), default=None)
    desc = db.Column(db.Unicode(), default=None)
    authors = db.Column(db.Unicode(), default=None)
    buy_url = db.Column(db.Unicode(), default=None)
    cover = db.Column(db.Unicode(), default=None)
    # tags = db.Column(db.Unicode(), default=None)
