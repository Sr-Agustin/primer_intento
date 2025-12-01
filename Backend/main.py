from fastapi import FastAPI
from routers.transcriptions import router as transcriptions_router

app = FastAPI()

app.include_router(transcriptions_router, prefix="/api")
