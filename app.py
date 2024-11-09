import os, sys
import pandas as pd
import numpy as np

import pymongo

import certifi
ca = certifi.where()

from dotenv import load_dotenv
load_dotenv()

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile,Request
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse

from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.pipeline.training_pipeline import TrainingPipeline

from networksecurity.utils.main_utils.utils import load_object
from networksecurity.utils.ml_utils.model.estimator import NetworkModel


mongo_db_url = os.getenv("MONGO_DB_URL")
print(mongo_db_url)


client = pymongo.MongoClient(mongo_db_url, tlsCAFile = ca)

from networksecurity.constant.training_pipeline import DATA_INGESTION_COLLECTION_NAME, DATA_INGESTION_DATABASE_NAME

database = client[DATA_INGESTION_COLLECTION_NAME]
collection = database[DATA_INGESTION_DATABASE_NAME]

app = FastAPI()
origins = ["*"]

# need to be accesed through browser
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory = "./templates")

# to create HOMEPAGE
@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("Training pipeline is successful")
    except Exception as e:
        raise NetworkSecurityException(e, sys)


if __name__== "__main__":
    app_run(app, host="localhost", port = 8000)



