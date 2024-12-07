
from fastapi import FastAPI

from app.api.endpoints.hotels import router

app = FastAPI()

app.include_router(router)


@app.get("/")
def home():
    """
    Welcome message for the API.
    """
    return {"message": "Welcome to booking API"}
