import time
from typing import Union


class Event:
    def __init__(self, data: Union[dict, None] = None, ttl=-1, expires_at=-1) -> None:
        if data:
            self._data = data
        else:
            self._data = {}
        self._ttl = ttl
        self._timestamp = time.time()
        if expires_at == -1 and self._ttl != -1:
            self._expires_at = self._timestamp + ttl
        else:
            self._expires_at = expires_at

    @property
    def timestamp(self) -> float:
        return self._timestamp

    @property
    def data(self) -> dict:
        return self._data

    def formated_data(self, format: dict) -> dict:
        result = {}
        for key, value_type in format.items():
            if key in self._data and type(self._data[key]) == value_type:
                result[key] = self._data[key]
            else:
                result[key] = None
        return result

    @staticmethod
    def formated_event_data(event, format: dict) -> dict:
        result = {}
        for key, value_type in format.items():
            if key in event and type(event[key]) == value_type:
                result[key] = event[key]
            else:
                result[key] = None
        return result

    @property
    def ttl(self) -> int:
        return self._ttl

    @property
    def expires_at(self) -> float:
        return self._expires_at

    @property
    def expired(self) -> bool:
        if self._ttl == -1 and self._expires_at == -1:
            return False
        else:
            return time.time() > self._expires_at
