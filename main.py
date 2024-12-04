from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from db.models import Base
from db.db_setup import engine

from auth import router as Auth_router
from user import router as User_router


Base.metadata.create_all(bind=engine)


API_TITLE = "RMW-API"
API_DESCRIPTION = "Ride my way"
API_VERSION = "1.1"

app = FastAPI(title=API_TITLE, description=API_DESCRIPTION, version=API_VERSION)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", tags=["Home"])
def home(request: Request):
    return templates.TemplateResponse(request=request, name="home.html", context={"title": API_TITLE})


app.include_router(Auth_router, prefix="/auth", tags=["Auth"])
app.include_router(User_router, prefix="/user", tags=["User"])
