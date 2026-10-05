from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.journal import journals

def get(db: Session, user_id: int):
    return db.execute(select(journals).where(journals.c.user_id == user_id).order_by(journals.c.created_at.desc())).mappings().all()