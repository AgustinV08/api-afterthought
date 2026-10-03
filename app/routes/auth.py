from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.controllers import auth_controller
from app.core.limiter import limiter
from app.database.database import get_db
from app.schemas.user import UserRead, UserCreate, UserSignin, UserLogin

authRouter = APIRouter()

@authRouter.post("/signup", response_model=UserRead, status_code=201)
@limiter.limit('10/minute')
def signup(request: Request, payload: UserCreate, db: Session = Depends(get_db)):
    return auth_controller.signup(db, payload)

@authRouter.post("/signin", response_model=UserSignin, status_code=200)
@limiter.limit('10/minute')
def signin(request: Request, payload: UserLogin, db: Session = Depends(get_db)):
    return auth_controller.signin(db, payload)

@authRouter.get("/user/me", response_model=UserRead, status_code=200)
@limiter.limit('10/minute')
def user_me(request: Request, db = Depends(get_db), token = Depends(auth_controller.auth_scheme)):
    return auth_controller.get_current_user(db, token)

@authRouter.post("/logout", status_code=204)
@limiter.limit('3/minute')
def logout(request: Request, db: Session = Depends(get_db), token = Depends(auth_controller.auth_scheme)):
    auth_controller.logout(db, token)