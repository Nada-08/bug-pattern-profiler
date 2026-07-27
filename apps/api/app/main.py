from fastapi import FastAPI
import os 
from apps.api.app.routers import health, chat

app = FastAPI(
    title="Bug Pattern Profiler API",
    version="0.1.0"
)


app.include_router(health.router)
app.include_router(chat.router)