from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import func

from .. import db


class Clusters(db.Model):
    __tablename__ = "clusters"

    id = db.Column(UUID, primary_key=True, server_default=func.uuid_generate_v4(), nullable=False)
    name = db.Column(db.Unicode(), default=None)
