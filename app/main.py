from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api import user_controller, organization_controller, document_controller, query_controller
from database.database import init_db

if __name__ == "main":
    init_db()
    print('Init db has been success')

app = FastAPI()

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

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
