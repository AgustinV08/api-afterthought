from sqlalchemy import Column, Integer, String, Float, MetaData, Table
from app.database.database import metadata

users = Table("users", metadata,
    id = Column(Integer, primary_key=True, index=True),
    name = Column(String(255), nullable=False),
    email = Column(String(255), nullable=False, unique=True),
    password = Column(String(255), nullable=True)
)
