import uvicorn
from fastapi import FastAPI
from src.api.v1.routers import router as main_router_v1


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(main_router_v1)
    return app


if __name__ == "__main__":
    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
