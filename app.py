from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from motor.motor_asyncio import AsyncIOMotorClient
import logging
from config.settings import logging_config, settings
from fill_db import example_form
from repositories import FormRepository
from services import FormService
import sys


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    A context manager that handles the FastAPI application's lifespan.

    The context manager is responsible for:

    1. Setting up logging
    2. Creating an async MongoDB client
    3. Creating an async MongoDB database
    4. Creating an async MongoDB collection
    5. Initializing the FormRepository and FormService
    6. Filling the database with example forms
    7. Yielding control to the application
    8. Cleaning up after the application is finished
    """
    try:
        logging_config("INFO")
        async_client = AsyncIOMotorClient(settings.URL_DATABASE)
        async_db = async_client[settings.DB_NAME]
        async_form_collection = async_db[settings.DB_COLLECTION]
        app.state.async_form_collection = async_form_collection
        form_repository = FormRepository(async_form_collection)
        form_service = FormService(form_repository)
        for form in example_form:
            await app.state.async_form_collection.update_one({"name": form["name"]}, {"$set": form}, upsert=True)
        yield
    except Exception as e:
        sys.exit(1)

app = FastAPI(lifespan=lifespan)
log = logging.getLogger(__name__)

@app.post("/get_form")
async def get_form(request: Request):
    form_service = FormService(FormRepository(app.state.async_form_collection))
    return await form_service.process_request(request)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)