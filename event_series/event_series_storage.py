from event_series import EventSeries


class EventSeriesStorage:
    def __init__(self) -> None:
        self._data: dict[str, EventSeries] = {}

    def add(self, key: str, timestamp: int, value: dict) -> None:
        if key not in self._data:
            self._data[key] = EventSeries()
        self._data[key].add(timestamp, value)

    def key_value_series(self, key: str, value: str) -> list:
        if key not in self._data:
            raise KeyError(f"Key {key} not found")
        return self._data[key].get(value)

    def value_series(self, value: str) -> dict:
        result = {}
        for key, series in self._data.items():
            data = series.get(value)
            if data:
                result[key] = data
        if not result:
            raise KeyError(f"Value {value} not found")
        return result

    def keys(self) -> list:
        return list(self._data.keys())

    def clear(self) -> None:
        self._data = {}
