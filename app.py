from starlette.responses import RedirectResponse
from fastapi import Request, HTTPException
from fastapi import FastAPI, Form, Request, UploadFile, File, Body
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import Cookie
from itsdangerous import URLSafeSerializer
import json
import sqlite3
import pandas as pd
import os


def connect():
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER,
        diagnosis TEXT
    )
    ''')

    cursor.execute('''
    INSERT INTO patients (name, age, diagnosis)
    VALUES (?, ?, ?)
    ''', ('John Doe', 30, 'Flu'))

    # Lưu thay đổi và đóng kết nối
    conn.commit()
    conn.close()


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/assets", StaticFiles(directory="assets"), name="assets")
templates = Jinja2Templates(directory='templates')
serializer = URLSafeSerializer('your-secret-key')


@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


@app.middleware("http")
async def session_middleware(request: Request, call_next):
    # Đọc session từ cookie nếu có
    session_data = request.cookies.get("session")
    if session_data:
        try:
            # Giải mã session data
            request.state.session = json.loads(serializer.loads(session_data))
        except:
            request.state.session = {}
    else:
        request.state.session = {}

    # Xử lý request
    response = await call_next(request)

    # Lưu session vào cookie
    if hasattr(request.state, "session"):
        session_data = serializer.dumps(json.dumps(request.state.session))
        response.set_cookie("session", session_data)

    return response

user = 'tien'


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
