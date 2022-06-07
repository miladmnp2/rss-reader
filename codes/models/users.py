import sqlalchemy

from db import metadata
from models.enums import RoleTypes

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("username", sqlalchemy.String(120), unique=True),
    sqlalchemy.Column("password", sqlalchemy.String(255)),
    sqlalchemy.Column("role", sqlalchemy.Enum(RoleTypes), nullable=False,
                      server_default=RoleTypes.reader.name),
)
