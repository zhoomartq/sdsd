from os import getenv

import motor.motor_asyncio
from fastapi import FastAPI

import db_cntx
import forms_router

app = FastAPI(
    description="API для создания и получения шаблонов форм."
)


@app.on_event("startup")
async def startup_event():
    client = motor.motor_asyncio.AsyncIOMotorClient(
        host=getenv("MONGO_HOST", "localhost"),
        port=int(getenv("MONGO_PORT", 27017)),
        username=getenv("MONGO_USERNAME", "root"),
        password=getenv("MONGO_PASSWORD", "password")
    )
    db_cntx.db = client.templates


app.include_router(forms_router.router)
