import time


class TimedEvent:
    def __init__(self, timestamp: int, data: dict) -> None:
        self._timestamp = timestamp
        self._data = data
        self._created_at = time.time_ns()

    @property
    def timestamp(self) -> int:
        return self._timestamp

    @property
    def data(self) -> dict:
        return self._data

    @property
    def created_at(self) -> int:
        return self._created_at

    @property
    def values(self) -> dict:
        return {"timestamp": self.timestamp, "data": self.data}

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return str(self.__dict__)

    def __eq__(self, te: object) -> bool:
        if isinstance(te, TimedEvent):
            return self._timestamp == te.timestamp and self._data == te.data

        return False

    def __lt__(self, te: object) -> bool:
        if isinstance(te, TimedEvent):
            if self._timestamp < te.timestamp:
                return True
            elif self._timestamp == te.timestamp:
                return self.created_at < te.created_at

        return False
