from fastapi import HTTPException
from sqlalchemy import select, insert
from sqlalchemy.orm import Session

from app.core.auth import hash_password, verify_password, create_access_token
from app.models.user import users
from app.schemas.user import UserCreate, UserLogin, UserSignin, UserRead


def create_user(db: Session, payload: UserCreate):
    result = db.execute(
        insert(users).values(
            name=payload.name,
            email=payload.email,
            password=hash_password(payload.password),
        )
    )
    db.commit()
    user_id = result.inserted_primary_key[0]

    return db.execute(
        select(users).where(users.c.id == user_id)
    ).mappings().first()

def signin(db: Session, payload: UserLogin) -> UserSignin:
    user = db.execute(
        select(users).where(users.c.email == payload.email)
    ).mappings().first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not verify_password(payload.password, user["password"]):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token(subject=str(user['id']))

    return UserSignin(access_token=token, email=user['email'], name=user['name'])