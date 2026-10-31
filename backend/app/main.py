"""Initialize the ViganGo FastAPI application and its endpoints."""

from fastapi import FastAPI

app = FastAPI(title="ViganGo API", version="0.1.0")


# Return the API's current health status.
@app.get("/health")
def health_check():
    return {"status": "ok"}
