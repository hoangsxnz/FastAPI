import json
import os
import shutil
import sqlite3 as lite
from pathlib import Path
from re import template
import queue
import cv2
from fastapi import Depends, FastAPI, File, Form, Request, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.config import Config
from starlette.requests import Request
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import HTMLResponse, RedirectResponse
from PIL import Image

import easy_ocr
from db_handler import *

# if database of accounts not exist then create, else add default accounts
if not os.path.exists('account_database.db'):
    create_info_default('account_database.db')
else:
    create_connection('account_database.db')


app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.mount("/static", StaticFiles(directory=Path(__file__).parent.absolute() /
                                 "static"), name="static",)
app.mount("/images", StaticFiles(directory=Path(__file__).parent.absolute() /
                                 "images"), name="static",)

templates = Jinja2Templates(directory="templates")

recent_images = queue.Queue()


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse('landing_page.html', {'request': request})


@app.get("/login")
async def login_screen(request: Request):
    return templates.TemplateResponse('login.html', {'request': request})


@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    con = lite.connect('account_database.db')
    cur = con.cursor()
    check_username_query = "SELECT username FROM account WHERE username = '{}'".format(
        username)
    cur.execute(check_username_query)
    print(cur.fetchone()[0])
    # if no username fetched then account not exist
    if cur.fetchone() == None:
        info = "Account not exist"
        return templates.TemplateResponse('login.html', {'request': request, 'info': info})
    else:
        # account exist, check input password
        check_password_query = 'SELECT password FROM login_info WHERE username =\'' + username + "\'"
        cur.execute(check_password_query)
        password_result = cur.fetchone()[0]

        # get role (in case correct password)
        check_role_query = 'SELECT role FROM login_info WHERE username =\'' + username + "\'"
        cur.execute(check_role_query)
        role_result = cur.fetchone()[0]

        if password_result != password:
            info = "Incorrect password"
            return templates.TemplateResponse("login.html", {"request": request, "username": username, "password": password, "info": info})
        else:
            # role admin, move to admin screen
            if role_result == 'admin':
                return templates.TemplateResponse('admin.html', {'request': request})
            # role user, move to user screen
            else:
                return templates.TemplateResponse('user.html', {'request': request})


@app.get("/admin")
async def admin_screen(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})


@app.post("/admin")
async def admin(image: UploadFile = File(...)):
    img = cv2.imread(image.filename)
    text = await easy_ocr.extract_text(img)
    return {"filename": image.filename, "text_detected": text}


@app.get("/user")
async def user_screen(request: Request):
    return templates.TemplateResponse("user.html", {"request": request})


@app.post("/user")
async def user(image: UploadFile = File(...)):
    img = cv2.imread(image.filename)
    text = await easy_ocr.extract_text(img)
    return {"filename": image.filename, "text_detected": text}


@app.get("/create_account")
async def create_account_screen(request: Request):
    return templates.TemplateResponse("create_account.html", {"request": request})


@app.post("/create_account")
async def create_account(request: Request, username: str = Form(...), password: str = Form(...), confirm_password: str = Form(...)):
    con = lite.connect('account_database.db')
    cur = con.cursor()
    sql_query = "'SELECT username FROM account WHERE username = '{}'".format(
        username)
    cur.execute(sql_query)
    # if no username fetched then account not exist -> create account
    if cur.fetchone():
        info = "Username is exist"
        return templates.TemplateResponse('create_account.html', {'request': request, "info": info})
    else:
        if password != confirm_password:
            info = 'Please check information of account.'
            return templates.TemplateResponse('create_account.html', {'request': request, "info": info})
        else:
            new_account = [username, password, 'user']
            cur.execute('INSERT INTO account VALUES(?, ?, ?)', new_account)
            info = 'Your account has been created. Return login!'
            con.commit()
            con.close()
            return templates.TemplateResponse('create_account.html', {'request': request, "info": info})


@app.get("/ocr")
async def ocr_screen(request: Request):
    return templates.TemplateResponse('user.html', {'request': request})


@app.post("/ocr")
async def ocr(image: UploadFile = File(...)):
    img = cv2.imread(image.filename)
    text = await easy_ocr.extract_text(img)
    return {"filename": image.filename, "text_detected": text}
