from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute

from app.routes import router

def version():
    return JSONResponse({"version": "v1"})


routes = [
    APIRoute("/", endpoint=version, response_class=JSONResponse),
]

app = FastAPI(
    routes=routes,
    title="Event Management APP",
    docs_url="/docs",
    redoc_url=None,
)

app.include_router(router, prefix="/api")