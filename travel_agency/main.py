from fastapi import FastAPI

from routers.tours import router

app = FastAPI(
    title="Sweet Travel API"
)

app.include_router(router)