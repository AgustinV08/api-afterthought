from sqlalchemy import Column, Integer, String, Float, MetaData, Table
from app.database.database import metadata

users = Table("users", metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("name", String(255), nullable=False),
    Column("email", String(255), nullable=False, unique=True),
    Column("password", String(255), nullable=False)
)
