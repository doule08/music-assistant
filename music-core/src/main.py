from pathlib import Path

from fastapi import FastAPI
from dotenv import load_dotenv
import uvicorn

from api.music_controller import router as music_router

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)

app = FastAPI()

app.include_router(music_router)


@app.get("/")
async def root():
    return {"message": "Hello from music-core!"}


if __name__ == "__main__":
    # Reload is set to True for development purposes; set it to False in production
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
