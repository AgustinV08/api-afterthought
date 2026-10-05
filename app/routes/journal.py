from fastapi import APIRouter, Depends

from app.controllers import journal_controller
from app.core.auth import get_current_user_id
from app.core.limiter import limiter
from app.database.database import get_db
from app.schemas.journal import JournalCreate

journalRouter = APIRouter()

@journalRouter.get("/", status_code=200)
def get(db = Depends(get_db), user_id = Depends(get_current_user_id)):
    return journal_controller.get(db, user_id)

@journalRouter.post("/", status_code=201)
def create(payload: JournalCreate, db = Depends(get_db), user_id = Depends(get_current_user_id)):
    return journal_controller.post(db, user_id, payload)