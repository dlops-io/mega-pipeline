import os
import asyncio
from fastapi import FastAPI, File
from starlette.middleware.cors import CORSMiddleware

from api.pipeline import PipelineManager
from api.routers import input_audios

# Pipeline Manager
pipeline_manager = PipelineManager()

# Setup FastAPI app
app = FastAPI(title="API Service", description="API Service", version="0.1.0")

# Enable CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=False,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    # Start tracker service
    asyncio.create_task(pipeline_manager.sync())


# Routes


@app.get("/", summary="Index", description="Root api")
async def get_index():
    return {"message": "API Server Running!"}


# Additional routers here
app.include_router(input_audios.router)
