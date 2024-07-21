import time

from fastapi import FastAPI, Request
from .routers import products, inventory
from .database import SessionLocal, engine
from .dynamodb import log_api_call
from .models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    log_api_call(request.url.path, response.status_code, process_time)
    return response


app.include_router(products.router)
app.include_router(inventory.router)
