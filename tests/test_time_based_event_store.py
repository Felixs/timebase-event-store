import unittest
from unittest.mock import patch
from event_store import TimeBaseEventStore
from event_store.timed_event import TimedEvent


class TestTimeBaseEventStore(unittest.TestCase):
    def test_time_based_event_store(self):
        tbes = TimeBaseEventStore()
        self.assertIsInstance(tbes, TimeBaseEventStore)

    def test_get_events_for_missing_key(self):
        tbes = TimeBaseEventStore()
        self.assertEqual(tbes.get("key"), None)

    def test_add_event(self):
        tbes = TimeBaseEventStore()
        tbes.add("key", 1, {"value": 1})
        self.assertEqual(tbes.get("key"), TimedEvent(1, {"value": 1}))

    def test_add_event_with_timestamp(self):
        tbes = TimeBaseEventStore()
        tbes.add("key", 1, {"value": 1})
        tbes.add("key", 2, {"value": 2})
        self.assertEqual(tbes.get("key"), TimedEvent(2, {"value": 2}))

    @patch("time.time_ns")
    def test_add_events_with_timestamp_out_of_order(self, mock_time):
        mock_time.return_value = 0
        tbes = TimeBaseEventStore()
        tbes.add("key", 2, {"value": 2})
        tbes.add("key", 1, {"value": 1})
        self.assertEqual(tbes.get("key"), TimedEvent(2, {"value": 2}))

    def test_add_events_with_same_timestamp_resolve_to_latest_insert(self):
        tbes = TimeBaseEventStore()
        tbes.add("key", 1, {"value": 2})
        tbes.add("key", 1, {"value": 3})
        tbes.add("key", 1, {"value": 1})
        self.assertEqual(tbes.get("key"), TimedEvent(1, {"value": 1}))

    def test_get_all_events_for_key(self):
        tbes = TimeBaseEventStore()
        tbes.add("key", 1, {"value": 1})
        tbes.add("key", 2, {"value": 2})
        self.assertEqual(
            tbes.get_all("key"), [{"timestamp": 1, "data": {"value": 1}}, {"timestamp": 2, "data": {"value": 2}}]
        )

    def test_get_all_events_for_key_out_of_order_inserts(self):
        tbes = TimeBaseEventStore()
        tbes.add("key", 1, {"value": 1})
        tbes.add("key", 2, {"value": 2})
        tbes.add("key", 0, {"value": 0})
        self.assertEqual(
            tbes.get_all("key"),
            [
                {"timestamp": 0, "data": {"value": 0}},
                {"timestamp": 1, "data": {"value": 1}},
                {"timestamp": 2, "data": {"value": 2}},
            ],
        )

    def test_get_all_events_for_missing_key(self):
        tbes = TimeBaseEventStore()
        self.assertEqual(tbes.get_all("key"), None)

    def test_get_first_event_for_missing_key(self):
        tbes = TimeBaseEventStore()
        self.assertEqual(tbes.get_first("key"), None)

    def test_get_first_event_for_key(self):
        tbes = TimeBaseEventStore()
        tbes.add("key", 1, {"value": 1})
        tbes.add("key", 2, {"value": 2})
        self.assertEqual(tbes.get_first("key"), TimedEvent(1, {"value": 1}))
