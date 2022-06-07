import sqlalchemy

from db import metadata

feeds = sqlalchemy.Table(
    "feeds",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String(300), unique=True),
    sqlalchemy.Column("link", sqlalchemy.String(255)),
    sqlalchemy.Column("description", sqlalchemy.Text),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, server_default=sqlalchemy.func.now()),
    sqlalchemy.Column("publisher_id", sqlalchemy.ForeignKey("publishers.id"), nullable=False)
)
