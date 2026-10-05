from sqlalchemy import Column, String, Table, DateTime, Integer, ForeignKey
from app.database.database import metadata

journals = Table("journals", metadata,
    Column("id", Integer, primary_key=True),
    Column("content", String, nullable=False),
    Column("created_at", DateTime, nullable=False),
    Column("updated_at", DateTime, nullable=False),
    Column("user_id", Integer, ForeignKey('users.id'), nullable=False)
)
