import os
import uuid
import jwt

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
from jwt.exceptions import InvalidTokenError

auth_scheme = OAuth2PasswordBearer(tokenUrl="auth/signin")
password_hash = PasswordHash.recommended()

SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

def hash_password(password: str) -> str:
    return password_hash.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return password_hash.verify(password, hashed)

def create_access_token(subject: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": subject, "exp": expire, "jti": uuid.uuid4().hex}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> str | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except InvalidTokenError as e:
        return None
    return payload.get("sub")


def decode_token_payload(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except InvalidTokenError:
        return None

def get_current_user_id (token: str = Depends(auth_scheme)):
    user_id = decode_access_token(token)
    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Token is invalid",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return int(user_id)