import asyncio
import logging
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api import (user_controller, organization_controller, document_controller, query_controller,
                 transactions_contoller, service_controller)
from database.database import init_db
from rabbitmq_consumer import start_consume

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="LLM",
    description="API description",
    version="1.0.0",
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
    swagger_ui_oauth2_redirect_url="/api/v1/docs/oauth2-redirect",
    swagger_ui_init_oauth2={
        "usePkceWithAuthorizationCodeGrant": True
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_controller.router, prefix="/api")
app.include_router(organization_controller.router, prefix="/api")
app.include_router(document_controller.router, prefix="/api")
app.include_router(query_controller.router, prefix="/api")
app.include_router(transactions_contoller.router, prefix="/api")
app.include_router(service_controller.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.on_event("startup")
async def startup_event():
    # init_db()
    # print('Init db has been success')
    asyncio.create_task(start_consume())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
