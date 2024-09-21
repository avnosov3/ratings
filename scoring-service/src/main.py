import uvicorn
from fastapi import FastAPI
from fastapi_pagination import add_pagination
from src.api.v1.routers import router as main_router_v1


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(main_router_v1)
    add_pagination(app)
    return app


if __name__ == "__main__":
    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
