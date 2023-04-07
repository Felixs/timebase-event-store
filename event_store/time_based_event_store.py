import time
from collections import defaultdict
from typing import List

from event_store.event import Event


class TimeBaseEventStore:
    def __init__(self) -> None:
        self._events = defaultdict(lambda: defaultdict(dict))

    def get(self, key: str) -> dict:
        if key in self._events:
            highest_timestamp = max(self._events[key].keys())
            highest_insert_time = max(self._events[key][highest_timestamp].keys())
            return self._events[key][highest_timestamp][highest_insert_time].data
        return {}

    def add(self, key: str, timestamp: float, event_data: dict) -> None:
        insert_time = time.time_ns()
        self._events[key][timestamp][insert_time] = Event(data=event_data)

    def get_first(self, key: str) -> dict:
        lowest_timestamp = min(self._events[key].keys())
        lowest_insert_time = min(self._events[key][lowest_timestamp].keys())
        return self._events[key][lowest_timestamp][lowest_insert_time].data

    def get_all(self, key: str) -> List[dict]:
        result = []
        for _, timestamp_entry in sorted(self._events[key].items()):
            for _, insert_time_entry in sorted(timestamp_entry.items()):
                result.append(insert_time_entry.data)

        return result

    def get_all_formated(self, key: str, format: dict) -> List[dict]:
        data = self.get_all(key)
        return [Event.formated_event_data(data_entry, format) for data_entry in data]
