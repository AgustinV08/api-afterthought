from sqlalchemy import Column, String, Table, DateTime
from app.database.database import metadata

revoked_tokens = Table("revoked_tokens", metadata,
    Column("jti", String(32), primary_key=True),
    Column("expires_at", DateTime, nullable=False, index=True)
)
