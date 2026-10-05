from fastapi import APIRouter, Depends, Request

from app.controllers import journal_controller
from app.controllers.auth_controller import auth_scheme
from app.core.auth import get_current_user_id
from app.core.limiter import limiter
from app.database.database import get_db

journalRouter = APIRouter()

@journalRouter.get("/", status_code=200)
def get(db = Depends(get_db), user_id = Depends(get_current_user_id)):
    return journal_controller.get(db, user_id)