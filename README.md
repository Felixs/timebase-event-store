# Stay a while and listen
Just playing around with Event Bases Storage and Retrieval (in-memory for now ;) ). Feel free to take a look around.

## Idea

The idea is to have a simple way to store and retrieve events and changes in an event timeline.
Events of a timeline can be given in any order and will be stored based on a given timestamp.
Events with the same timestamp will be stored in the order they are inserted.
Event timelines can be identified by a unique identifier (key).
Events contain any dict as data.

The timeline event data is based on any key in any of the events data. So changes in timeline data can be tracked and retrieved.

Example input:
```
{"timestamp": 1680945987, "data": {"key": "start"}}
{"timestamp": 1680945989, "data": {"key": "wait"}}
{"timestamp": 1680946010, "data": {"key": "wait"}}
{"timestamp": 1680946015, "data": {"key": "end"}}
```

Example output could look like:
```
[(1680945987, "start"), (1680945989, "wait"), (1680946010, "wait"), (1680946015, "end")]
```
### Problems:
- What to do with events that have the same data, add it to the timeline change or leave it out?
    - Maybe have sperate ways to retrieve the data, one with only the changing date points and one with all the data points? 
- What to do with events that miss the expected data key?
    - Logicaly missing data would mean no change in the timeline, so leave them out in changing data points and add them with previous data in continous data timelines. 
- How to search in the storage for a specific event key value data?
- How to retieve all data changes from a specific event key value data?
- How to retieve all data changes to a specific event key value data?
- Why not simple use a timebased database like InfluxDB or TimescaleDB?
    - Because the idea is aggregate the data of many timelines. A.e. all changes from start to wait in the last 10 minutes. Or what was the next status for all wait events given a certain timeframe.

## Installation

### Requirements
- Python 3.10+

### In virtual environment
```shell
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Run
```uvicorn main:app --reload```

### Helpers

Run test and create coverage file:

```coverage run -m pytest```

Inline coverage overview:

```coverage report -m```

HTML coverage report:

```coverage html```