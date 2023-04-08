from typing import Any, List

from event_store.timed_event import TimedEvent


class TimedEventSeries:
    def __init__(self) -> None:
        self._data: List[TimedEvent] = []
        self._transition_cache: dict = {}

    @property
    def data(self) -> List[TimedEvent]:
        return self._data

    @property
    def version(self) -> int:
        return len(self._data)

    def add(self, event: TimedEvent) -> None:
        self._data.append(event)
        self._data.sort()
        self._invalidate_cache()

    def get(self) -> TimedEvent:
        return self._data[-1]

    def get_first(self) -> TimedEvent:
        return self._data[0]

    def get_all(self) -> List[TimedEvent]:
        return self._data

    def contains(self, key: str, values: Any) -> bool:
        for event in self._data:
            if key in event.data and event.data[key] == values:
                return True
        return False

    def changes_to(self, key: str, values: Any) -> bool:
        for event in self._data:
            if key in event.data and event.data[key] != values:
                return True
        return False

    def get_transition(self, key: str) -> List[str]:
        cache_key = f"{TimedEventSeries.get_transition.__name__}__{key}"
        if cache_key not in self._transition_cache:
            self._transition_cache[cache_key] = self._build_transition_for_key(key)

        return self._transition_cache[cache_key]

    def get_all_transitions(self) -> dict:
        cache_key = TimedEventSeries.get_all_transitions.__name__
        if cache_key not in self._transition_cache:
            self._transition_cache[cache_key] = self._build_all_transitions()
        return self._transition_cache[cache_key]

    def _build_transition_for_key(self, key):
        changes = []
        for event in self._data:
            if key in event.data:
                changes.append(event.data[key])
        return changes

    def _build_all_transitions(self):
        changes = {}
        for event in self._data:
            for key, value in event.data.items():
                if key not in changes:
                    changes[key] = [value]
                else:
                    changes[key].append(value)
        return changes

    def _invalidate_cache(self):
        self._transition_cache = {}

    def to_time_series(self, formating: dict) -> List[Any]:
        result = []
        for event in self._data:
            entry = []
            for key, value in formating.items():
                if key in event.data and type(event.data[key]) == value:
                    entry.append(event.data[key])
            result.append(tuple(entry))
        return result

    # def _next(self, key: str, value: Any) -> Any:
    #     for event in self._data:
    #         if key in event.data and event.data[key] != value:
    #             return event.data[key]
    #     return None
