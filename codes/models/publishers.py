import sqlalchemy

from db import metadata

publishers = sqlalchemy.Table(
    "publishers",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(120), unique=True),
    sqlalchemy.Column("link", sqlalchemy.String(255), nullable=False),
    sqlalchemy.Column("description", sqlalchemy.Text),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, server_default=sqlalchemy.func.now())
)
