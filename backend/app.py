from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.health import router as health_router


app = FastAPI(
    title="IT Operations Automation Platform",
    description="Web API for the Python IT Operations Automation Toolkit",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(health_router)


@app.get("/")
def root():
    return {
        "message": "IT Operations Automation Platform API",
        "status": "online"
    }


@app.get("/api")
def api_status():
    return {
        "name": "IT Operations Automation Platform",
        "version": "1.0.0",
        "status": "online"
    }