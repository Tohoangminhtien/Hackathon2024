from fastapi import Request
from fastapi.responses import RedirectResponse
from fastapi import FastAPI, Form, Request, File, Body
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import pandas as pd
import os
from utils.common import *
from dotenv import load_dotenv


app = FastAPI()
app.mount("/assets", StaticFiles(directory="assets"), name="assets")
templates = Jinja2Templates(directory='templates')

user = 'To Hoang Minh Tien'


@app.get("/")
async def main_page(request: Request):
    return templates.TemplateResponse('home.html', {"request": request,
                                                    "patient": user})


@app.get("/history")
async def get_history(request: Request):
    history = [f for f in os.listdir(f"data/{user}")]
    dataframes = dict()
    for i in history:
        df = pd.read_csv(f"data/{user}/{i}")
        dataframes.update({i: df.to_dict(orient="records")})

    return templates.TemplateResponse('history.html', {"request": request, "dataframes": dataframes})


@app.get("/chat")
def redirect():
    return RedirectResponse(url="http://localhost:8501/")
