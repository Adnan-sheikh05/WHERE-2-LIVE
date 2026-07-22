from fastapi import FastAPI
from sqlmodel import SQLModel
from sqlalchemy.exc import OperationalError
from database import engine
from routers import cities , auth , rankings , ai , comparisions
from middlewares.logging_middleware import log_requests 

app = FastAPI()


# DB Connection
@app.on_event("startup")
def on_start_up() :
    try :
        SQLModel.metadata.create_all(engine)
        print("Database Connected Successfully!")
    except OperationalError as e :
        print("DB CONNECTION FAILED : " , e)



@app.get("/")
def home():
    return {"message" : "WELCOME TO WHERE TO LIVE API 1.0"}

app.include_router(cities.router)
app.include_router(auth.router)
app.include_router(rankings.router)
app.include_router(ai.router)
app.include_router(comparisions.router)


# Loggin Middlware
app.middleware('http')(log_requests)