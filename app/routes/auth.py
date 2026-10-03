from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controllers import auth_controller
from app.database.database import get_db
from app.schemas.user import UserRead, UserCreate, UserSignin, UserLogin

authRouter = APIRouter()

@authRouter.post("/signup", response_model=UserRead, status_code=201)
def signup(payload: UserCreate, db: Session = Depends(get_db)):
    return auth_controller.create_user(db, payload)

@authRouter.post("/signin", response_model=UserSignin, status_code=200)
def signin(payload: UserLogin, db: Session = Depends(get_db)):
    return auth_controller.signin(db, payload)

@authRouter.get("/user/me", response_model=UserRead, status_code=200)
def user_me(current_user = Depends(auth_controller.get_current_user)):
    return current_user

@authRouter.post("/logout", status_code=204)
def logout(db: Session = Depends(get_db), token = Depends(auth_controller.auth_scheme)):
    auth_controller.logout(db, token)