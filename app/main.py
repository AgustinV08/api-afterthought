from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database.database import Base, engine
from app.routes.auth import authRouter
from app.routes.routes import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(router)
app.include_router(authRouter, prefix="/auth", tags=["auth"])
