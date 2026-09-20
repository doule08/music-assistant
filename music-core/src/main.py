from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn

from api.music_controller import router as music_router
from infrastructure.http.clients import create_http_client_factory
from infrastructure.mqtt.mqtt_subscriber import MqttSubscriber


@asynccontextmanager
async def lifespan(app: FastAPI):
    http_client_factory = create_http_client_factory()
    mqtt_subscriber = MqttSubscriber()

    await http_client_factory.start()
    mqtt_subscriber.start()

    # Store the http_client_factory in the app state so it can be accessed in the dependencies
    app.state.http_client_factory = http_client_factory
    app.state.mqtt_subscriber = mqtt_subscriber

    try:
        # Yield control back to the FastAPI application to handle requests
        yield
    finally:
        mqtt_subscriber.stop()
        await http_client_factory.close()


app = FastAPI(lifespan=lifespan)

app.include_router(music_router)


@app.get("/")
async def root():
    return {"message": "Hello from music-core!"}


if __name__ == "__main__":
    # Keep reload disabled while using MQTT in development; the reloader creates duplicate clients and reconnect loops.
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
