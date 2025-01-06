from fastapi import FastAPI
from api.endpoints import earthquakes, analysis
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="API Gateway")

@app.on_event("startup")
async def startup_event():
    env_vars = {k: '***' if 'key' in k.lower() else v for k, v in os.environ.items()}
    logger.info(f"Environment variables: {env_vars}")

app.include_router(earthquakes.router, prefix="/api/v1")
app.include_router(analysis.router, prefix="/api/v1")
