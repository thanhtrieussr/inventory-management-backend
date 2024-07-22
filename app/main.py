# app/main.py
# Author: Thanh Trieu
# Description: Main entry point for the FastAPI application, including middleware, routers, and AWS Lambda integration.

import time
from fastapi import FastAPI, Request
from mangum import Mangum

from .database import SessionLocal, engine
from .dynamodb import log_api_call
from .models import Base
from .routers import products, inventory, orders

# Create the database tables if they don't already exist
Base.metadata.create_all(bind=engine)

# Initialize the FastAPI application
app = FastAPI()

# Dependency function to get a database session
def get_db():
    """Provides a database session for dependency injection."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Middleware to measure and log the processing time of each request
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Middleware to calculate and log the request processing time."""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    log_api_call(request.url.path, response.status_code, process_time)
    return response

# Include the routers for the different API endpoints
app.include_router(products.router)
app.include_router(inventory.router)
app.include_router(orders.router)

# Create the Mangum handler to run the FastAPI app on AWS Lambda
lambda_handler = Mangum(app)
