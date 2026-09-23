from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.health import router as health_router


app = FastAPI(
    title="IT Operations Automation Platform",
    description="Web API for the Python IT Operations Automation Toolkit",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(health_router)


@app.get("/")
def root():
    return {
        "message": "IT Operations Automation Platform API",
        "status": "online",
    }


@app.get("/api")
def api_status():
    return {
        "name": "IT Operations Automation Platform",
        "version": "1.0.0",
        "status": "online",
    }


@app.get("/api/endpoints", tags=["API"])
def list_endpoints():
    """Return the HTTP routes currently registered with the application."""
    endpoints = []

    for route in app.routes:
        methods = getattr(route, "methods", None)
        path = getattr(route, "path", None)

        if not methods or not path:
            continue

        endpoints.append({
            "path": path,
            "methods": sorted(methods),
        })

    return {"endpoints": sorted(endpoints, key=lambda endpoint: endpoint["path"])}


@app.on_event("startup")
async def log_registered_endpoints():
    """Print the registered API routes when the backend starts."""
    print("Registered API endpoints:")

    for endpoint in list_endpoints()["endpoints"]:
        methods = ", ".join(endpoint["methods"])
        print(f"  {methods:<12} {endpoint['path']}")
