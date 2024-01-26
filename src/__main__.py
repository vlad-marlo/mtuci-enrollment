from fastapi import FastAPI
from .api import routers

app = FastAPI(title="TODO enrollment app")

for router in routers:
    app.include_router(router, prefix="/api/v1")
