from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


API_TITLE = "RMW-API"
API_DESCRIPTION = "Ride my way"
app = FastAPI(title=API_TITLE, description=API_DESCRIPTION)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(request=request, name="home.html", context={"title": API_TITLE})
