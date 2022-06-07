import sqlalchemy

from db import metadata

seen = sqlalchemy.Table(
    "seen",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, server_default=sqlalchemy.func.now()),
    sqlalchemy.Column("user_id", sqlalchemy.ForeignKey("users.id"), nullable=False),
    sqlalchemy.Column("feed_id", sqlalchemy.ForeignKey("feeds.id"), nullable=False)
)
