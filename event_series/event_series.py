import bisect
from collections import defaultdict
from typing import Any, Dict, List, Set, Tuple


class EventSeries:
    def __init__(self) -> None:
        self._data: Dict[str, List[Tuple[int, Any]]] = defaultdict(list)

    def add(self, timestamp: int, event: Dict[str, Any]) -> None:
        flat_event = self.flatten_dict(event)
        for key, value in flat_event.items():
            bisect.insort(self._data[key], (timestamp, value))

    def get(self, key: str) -> List[Tuple[int, Any]]:
        if key not in self._data:
            return []
        return self._data[key]

    def get_keys(self) -> Set[str]:
        return set(self._data.keys())

    def clear(self) -> None:
        self._data = defaultdict(list)

    @staticmethod
    def flatten_dict(event: Dict[str, Any], prefix: str = "") -> Dict[str, Any]:
        flat_event = {}
        for key, value in event.items():
            if isinstance(value, dict):
                flat_event.update(__class__.flatten_dict(value, prefix + key + "."))
            else:
                flat_event[prefix + key] = value
        return flat_event
