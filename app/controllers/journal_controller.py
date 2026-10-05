from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.journal import journals
from app.schemas.journal import JournalCreate


def get(db: Session, user_id: int):
    return db.execute(select(journals).where(journals.c.user_id == user_id).order_by(journals.c.created_at.desc())).mappings().all()

def post(db: Session, user_id: int, payload: JournalCreate):
    try:
        result = db.execute(insert(journals).values(content=payload.content, user_id=user_id))
    except IntegrityError as error:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(error))
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(status_code=422, detail=str(error))

    query = db.execute(select(journals).where(journals.c.id == result.inserted_primary_key[0])).mappings().first()
    db.commit()

    return query