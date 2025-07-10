from fastapi import FastAPI, Request, Response , HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.router import emotion_router, webhook
from dotenv import load_dotenv
import os

load_dotenv()


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("CORS_ORIGIN")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health Check
@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(emotion_router.emotion_router, prefix="/emotion")
app.include_router(webhook.router, prefix="/webhook")

