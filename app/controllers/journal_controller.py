from sqlalchemy import select
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.orm import Session

from app.models.journal import journals
from app.schemas.journal import JournalCreate


def get(db: Session, user_id: int):
    return db.execute(select(journals).where(journals.c.user_id == user_id).order_by(journals.c.created_at.desc())).mappings().all()

def post(db: Session, user_id: int, payload: JournalCreate):
    result = db.execute(insert(journals).values(content=payload.content, user_id=user_id))
    query = db.execute(select(journals).where(journals.c.id == result.inserted_primary_key[0])).mappings().first();
    db.commit()

    return query