from contextlib import asynccontextmanager

from app.agent import build_agent
from app.webhook import router as webhook_router
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    build_agent()
    yield


app = FastAPI(title="Facebook Auto Reply Bot", lifespan=lifespan)
app.include_router(webhook_router)


@app.get("/")
def root():
    return {"status": "ok"}