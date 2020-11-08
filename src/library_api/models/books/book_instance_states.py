from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import func, CheckConstraint

from .. import db
from .book_instances import BookInstances
from ..clusters.clusters import Clusters
from ..users.users import Users


class BookInstanceStates(db.Model):
    __tablename__ = "book_instance_states"

    id = db.Column(UUID, primary_key=True, server_default=func.uuid_generate_v4(), nullable=False)
    action_date = db.Column(db.DateTime(), server_default=func.now(), nullable=False)
    book_instance_id = db.Column(UUID, db.ForeignKey(BookInstances.id), nullable=False)
    user_id = db.Column(UUID, db.ForeignKey(Users.id))
    cluster_id = db.Column(UUID, db.ForeignKey(Clusters.id))
    CheckConstraint('num_nonnulls(user, cluster) = 1', name='check_cluster_or_user')
    _user_id_idx = db.Index('index_on_user_id', 'user_id')
    _book_instance_id_idx = db.Index('index_on_book_instance_id', 'book_instance_id')
