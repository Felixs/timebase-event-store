from time import time

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from event_series import EventSeries

app = FastAPI()
series = EventSeries()


class Event(BaseModel):
    timestamp: int | None = None
    data: dict


# TODO info about the api? maybe link to docs and github
@app.get("/")
async def root():
    return {"message": "Hello World"}


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

    return {"data": series.get(key)}


@app.delete("/reset")
async def reset():
    series.clear()
    return 200


def create_app():
    return app


def cleanup():
    series.clear()
