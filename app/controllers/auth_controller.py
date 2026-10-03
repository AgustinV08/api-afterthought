from datetime import datetime, timezone

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select, insert, delete
from sqlalchemy.orm import Session

from app.core.auth import hash_password, verify_password, create_access_token, decode_access_token, decode_token_payload
from app.database.database import get_db
from app.models.revoked_token import revoked_tokens
from app.models.user import users
from app.schemas.user import UserCreate, UserLogin, UserSignin, UserRead

auth_scheme = OAuth2PasswordBearer(tokenUrl="auth/signin")

def signup(db: Session, payload: UserCreate):
    user_exists = db.execute(select(users).where(users.c.email == payload.email)).scalar()

    if user_exists is not None:
        raise HTTPException(
            status_code=400,
            detail="Email already registered",
        )

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

def get_current_user(token: str = Depends(auth_scheme), db: Session = Depends(get_db)):
    credentials_error = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_token_payload(token)
    if payload is None or "jti" not in payload:
        raise credentials_error

    revoked = db.execute(
        select(revoked_tokens.c.jti).where(revoked_tokens.c.jti == payload["jti"])
    ).first()
    if revoked:
        raise credentials_error

    user = db.execute(
        select(users).where(users.c.id == int(payload["sub"]))
    ).mappings().first()

    if user is None:
        raise credentials_error

    return user

def logout(db: Session, token: str = Depends(auth_scheme)):
    payload = decode_token_payload(token)

    revoked = db.execute(select(revoked_tokens).where(revoked_tokens.c.jti == payload["jti"])).first()

    if revoked is not None:
        raise HTTPException(
            status_code=401,
            detail="Token already expired",
            headers={"WWW-Authenticate": "Bearer"},
        )

    expires_at = datetime.fromtimestamp(payload["exp"], tz=timezone.utc).replace(tzinfo=None)

    db.execute(insert(revoked_tokens).values(jti=payload["jti"], expires_at=expires_at))

    db.execute(delete(revoked_tokens).where(revoked_tokens.c.expires_at < datetime.now(tz=timezone.utc)))
    db.commit()

    return {'message': 'You have been logged out'}