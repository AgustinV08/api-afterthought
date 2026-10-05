from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
import logging

from app.core.limiter import limiter
from app.database.database import Base, engine
from app.routes.auth import authRouter
from app.routes.journal import journalRouter
from app.routes.routes import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

logger = logging.getLogger(__name__)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(router)
app.include_router(authRouter, prefix="/api/auth", tags=["api.auth"])
app.include_router(journalRouter, prefix="/api/journal", tags=["api.journal"])

@app.exception_handler(RequestValidationError)
async def validation_handler(request: Request, exc: RequestValidationError):
    errors = {
        ".".join(str(p) for p in e["loc"][1:]): e["msg"]
        for e in exc.errors()
    }
    return JSONResponse(status_code=422, content={"errors": errors})

@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled error on %s %s, Error: %s", request.method, request.url.path, exc)
    return JSONResponse(status_code=500, content={'detail': 'Internal Server Error'})
