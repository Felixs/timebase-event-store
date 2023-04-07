from collections import defaultdict
from typing import List

from event_store.timed_event import TimedEvent


# TODO: rename: TimeBaseEventStore -> TimedEventStore
class TimeBaseEventStore:
    def __init__(self) -> None:
        self._events = defaultdict(lambda: [])

    def add(self, key: str, timestamp: int, event_data: dict) -> None:
        event = TimedEvent(timestamp=timestamp, data=event_data)
        self._events[key].append(event)
        self._events[key].sort()

    def get(self, key: str) -> TimedEvent | None:
        if key in self._events:
            return self._events[key][-1]

        return None

    def get_first(self, key: str) -> TimedEvent | None:
        if key in self._events:
            return self._events[key][0]

        return None

    def get_all(self, key: str) -> List[TimedEvent] | None:
        if key in self._events:
            return [event.values for event in self._events[key]]

        return None
