from time import time

from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from .definitions import FASTAPI_CONFIG

from event_series import EventSeries, EventSeriesStorage
from event_series.tools import image_bytes_from_event_value

app = FastAPI(**FASTAPI_CONFIG)
series = EventSeries()
storage = EventSeriesStorage()


class Event(BaseModel):
    timestamp: int | None = None
    data: dict


@app.get("/")
async def root():
    html = """<!DOCTYPE html>
    <html>
        <head>
            <title>Event Series API</title>
        </head>
        <body>
            <h1>Event Series API</h1>
            <p>See the <a href="https://github.com/Felixs/timebase-event-store">github repo</a> for more information.</p>
            <h2>Documentation</h2>
            <p>See the <a href="/docs">docs</a> for Swagger UI</p>
        </body>
    </html>"""
    return HTMLResponse(content=html, status_code=200)


@app.post("/event")
async def add_event(event: Event):
    if event.timestamp is None:
        timestamp = int(time())
        series.add(timestamp, event.data)
    else:
        series.add(event.timestamp, event.data)
    return 200


@app.get("/event/{key}")
async def get_event(key: str):
    series_data = series.get(key)
    if not series_data:
        raise HTTPException(status_code=404, detail="No data for key")

    return {"data": series_data}


@app.post("/events/{id}")
async def add_event_by_id(id: str, event: Event):
    if event.timestamp is None:
        timestamp = int(time())
        storage.add(id, timestamp, event.data)
    else:
        storage.add(id, event.timestamp, event.data)
    return 200


@app.get("/events/{id}/{value}")
async def get_event_by_id(id: str, value: str):
    try:
        series_data = storage.key_value_series(id, value)
        if not series_data:
            raise HTTPException(status_code=404, detail=f"No data for value {value}")

        return {"data": series_data}
    except KeyError:
        raise HTTPException(status_code=404, detail=f"No data for id {id}")


@app.get("/values/{value}")
async def get_values(value: str):
    try:
        series_data = storage.value_series(value)
        return {"data": series_data}
    except KeyError:
        raise HTTPException(status_code=404, detail=f"No data for value {value}")


@app.get("/visualize/{id}/{value}", responses={200: {"content": {"image/png": {}}}}, response_class=Response)
async def visualize(id: str, value: str):
    data = await get_event_by_id(id, value)
    try:
        image = image_bytes_from_event_value(f"{id} - {value}", data["data"])
    except ValueError:
        raise HTTPException(status_code=404, detail=f"No data for value {value}")
    return Response(content=image, media_type="image/png")


@app.delete("/reset")
async def reset():
    cleanup()
    return 200


def create_app():
    return app


def cleanup():
    series.clear()
    storage.clear()
