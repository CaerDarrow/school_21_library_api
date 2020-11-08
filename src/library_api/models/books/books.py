from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy import func

from .. import db


class Books(db.Model):
    __tablename__ = "books"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._instances = set()
        self._tags = set()

    id = db.Column(UUID, primary_key=True, server_default=func.uuid_generate_v4(), nullable=False)
    name = db.Column(db.Unicode(), default=None)
    desc = db.Column(db.Unicode(), default=None)
    authors = db.Column(db.Unicode(), default=None)
    buy_url = db.Column(db.Unicode(), default=None)
    edition_number = db.Column(db.Integer(), default=None)
    edition_year = db.Column(db.Integer(), default=None)
    cover_url = db.Column(db.Unicode(), default=None)

    @property
    def instances(self):
        return self._instances

    @instances.setter
    def instances(self, value):
        self._instances.add(value)

    @property
    def tags(self):
        return self._tags

    @tags.setter
    def tags(self, value):
        self._tags.add(value)
