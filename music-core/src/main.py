from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI
from dotenv import load_dotenv
import uvicorn

from api.music_controller import router as music_router
from infrastructure.http.clients import create_http_client_factory


@asynccontextmanager
async def lifespan(app: FastAPI):
    http_client_factory = create_http_client_factory()

    await http_client_factory.start()

    app.state.http_client_factory = http_client_factory

    try:
        yield
    finally:
        await http_client_factory.close()


env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)


app = FastAPI(lifespan=lifespan)

app.include_router(music_router)


@app.get("/")
async def root():
    return {"message": "Hello from music-core!"}


if __name__ == "__main__":
    # Reload is set to True for development purposes; set it to False in production
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
