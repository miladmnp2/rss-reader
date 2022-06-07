import sqlalchemy

from db import metadata

subscribers = sqlalchemy.Table(
    "subscribers",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, server_default=sqlalchemy.func.now()),
    sqlalchemy.Column("user_id", sqlalchemy.ForeignKey("users.id"), nullable=False),
    sqlalchemy.Column("publisher_id", sqlalchemy.ForeignKey("publishers.id"), nullable=False)
)
