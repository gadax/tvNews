from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from migration import migration 


app = FastAPI()
cur = migration.init()
app.mount("/templates", StaticFiles(directory="templates"), name="static")
tjinja = Jinja2Templates(directory="templates")


@app.get("/")
async def app_shell(request: Request):
    return tjinja.TemplateResponse('index.html', {"request": request})

@app.get("/ping")
async def ping():
    return {"msg": "pong"}

@app.get("/news/all")
async def select():
    sql = "SELECT * FROM news LIMIT 50"
    cur.execute(sql)

    return JSONResponse(cur.fetchall())

@app.get("/news/{id}")
async def select_one(id):
    id = int(id)
    sql = f"SELECT * FROM news WHERE id={id}"
    cur.execute(sql)

    return JSONResponse(cur.fetchall())