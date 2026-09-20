from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn

from api.music_controller import router as music_router
from infrastructure.http.clients import create_http_client_factory
from infrastructure.mqtt.mqtt_subscriber import MqttSubscriber


@asynccontextmanager
async def lifespan(app: FastAPI):
    http_client_factory = create_http_client_factory()

    await http_client_factory.start()

    # Store the http_client_factory in the app state so it can be accessed in the dependencies
    app.state.http_client_factory = http_client_factory

    try:
        # Yield control back to the FastAPI application to handle requests
        yield
    finally:
        await http_client_factory.close()


app = FastAPI(lifespan=lifespan)

app.include_router(music_router)


@app.get("/")
async def root():
    return {"message": "Hello from music-core!"}


if __name__ == "__main__":
    # Reload is set to True for development purposes; set it to False in production
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

    subscriber = MqttSubscriber()

    subscriber.start()
