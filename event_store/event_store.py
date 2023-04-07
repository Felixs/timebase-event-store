from collections import defaultdict
from typing import List, Tuple

from event_store.event import Event


class EventStore:
    def __init__(self) -> None:
        self._events: dict[str, dict[int, Event]] = defaultdict(dict)
        self._expired_events: List[Tuple[str, dict[int, Event]]] = []

    def add(self, key: str, event_data: dict) -> None:
        version = self._get_next_key_version(key)
        self._events[key][version] = Event(data=event_data)

    def get(self, key: str) -> dict:
        if key in self._events:
            event = self._events[key][self._get_latest_key_version(key)]
            if not event.expired:
                return event.data
            else:
                self._expired_events.append((key, self._events[key]))
                self.delete(key)

        return {}

    def get_all(self, key: str) -> List[dict]:
        if key in self._events and self.get(key):
            return [self._events[key][version].data for version in self._events[key] if self._events[key][version]]
        else:
            return []

    def get_all_format(self, key: str, format: dict) -> List[dict]:
        if key in self._events:
            data = self._events[key]
            return [entry.formated_data(format) for entry in data.values()]

        return []

    def get_expired(self, key: str) -> List[dict]:
        return [data[1] for data in self._expired_events if data[1] == key]

    def get_version(self, key: str, version: int) -> dict:
        if key in self._events:
            if version in self._events[key]:
                return self._events[key][version].data
        return {}

    def keys(self) -> List[str]:
        return list(self._events.keys())

    def expired_keys(self) -> List[str]:
        return list(set([key for key, _ in self._expired_events]))

    def delete(self, key: str) -> bool:
        if key in self._events:
            del self._events[key]
            return True
        return False

    def _get_next_key_version(self, key: str) -> int:
        if key in self._events:
            return self._get_latest_key_version(key) + 1
        return 0

    def _get_latest_key_version(self, key: str) -> int:
        if key in self._events:
            return max(self._events[key].keys())
        return -1
