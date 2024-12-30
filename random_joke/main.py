import requests
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    joke = await get_random_joke()
    return templates.TemplateResponse("index.html", {"request": request, "joke": joke})


async def get_random_joke():
    random_joke = requests.get("https://official-joke-api.appspot.com/random_joke")
    return random_joke.json()
