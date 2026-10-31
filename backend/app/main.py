"""Initialize the ViganGo FastAPI application and its endpoints."""

from fastapi import FastAPI

from app.routers.auth import router as auth_router

app = FastAPI(title="ViganGo API", version="0.1.0")
app.include_router(auth_router)


# Return the API's current health status.
@app.get("/health")
def health_check():
    return {"status": "ok"}
