import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from db.models import Base
from db.db_setup import engine, SessionLocal

from auth import router as Auth_router
from user import router as User_router
from rides import router as Ride_router
from dashboard.router import router as Dashboard_router
from management.router import router as Management_router
from rides.helpers import auto_update_expired_rides_and_requests

from config import ALLOWED_ORIGINS


Base.metadata.create_all(bind=engine)


API_TITLE = "RMW-API"
API_DESCRIPTION = "Ride my way"
API_VERSION = "1.1"


async def periodic_update_expired_rides_and_requests(interval_seconds: int = 60):
    """Background task loop (cron job) running periodically to check & update expired rides and requests."""
    while True:
        try:
            db = SessionLocal()
            try:
                auto_update_expired_rides_and_requests(db)
            finally:
                db.close()
        except Exception:
            pass
        await asyncio.sleep(interval_seconds)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start periodic background cron job
    task = asyncio.create_task(periodic_update_expired_rides_and_requests(interval_seconds=60))
    yield
    # Clean up background task on shutdown
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass


app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
    lifespan=lifespan,
)


# Setup cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", tags=["Home"])
def home(request: Request):
    return templates.TemplateResponse(request=request, name="home.html", context={"title": API_TITLE})


app.include_router(Auth_router, prefix="/auth", tags=["Auth"])
app.include_router(User_router, prefix="/user", tags=["User"])
app.include_router(Ride_router, prefix="/rides", tags=["Ride"])
app.include_router(Dashboard_router, prefix="/dashboard", tags=["Dashboard"])
app.include_router(Management_router, prefix="/management", tags=["Management"])