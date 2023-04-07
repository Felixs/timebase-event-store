import unittest
from event_store import TimeBaseEventStore


class TestTimeBaseEventStore(unittest.TestCase):
    def test_time_based_event_store(self):
        tbes = TimeBaseEventStore()
        self.assertIsInstance(tbes, TimeBaseEventStore)

    def test_get_events_for_missing_key(self):
        tbes = TimeBaseEventStore()
        self.assertEqual(tbes.get("key"), {})

    def test_add_event(self):
        tbes = TimeBaseEventStore()
        tbes.add("key", 1, {"value": 1})
        self.assertEqual(tbes.get("key"), {"value": 1})

    def test_add_event_with_timestamp(self):
        tbes = TimeBaseEventStore()
        tbes.add("key", 1, {"value": 1})
        tbes.add("key", 2, {"value": 2})
        self.assertEqual(tbes.get("key"), {"value": 2})

    def test_add_events_with_timestamp_out_of_order(self):
        tbes = TimeBaseEventStore()
        tbes.add("key", 2, {"value": 2})
        tbes.add("key", 1, {"value": 1})
        self.assertEqual(tbes.get("key"), {"value": 2})

    def test_add_events_with_same_timestamp_resolve_to_latest_insert(self):
        tbes = TimeBaseEventStore()
        tbes.add("key", 2, {"value": 2})
        tbes.add("key", 2, {"value": 3})
        tbes.add("key", 2, {"value": 1})
        self.assertEqual(tbes.get("key"), {"value": 1})

    def test_get_all_events_for_key(self):
        tbes = TimeBaseEventStore()
        tbes.add("key", 1, {"value": 1})
        tbes.add("key", 2, {"value": 2})
        self.assertEqual(tbes.get_all("key"), [{"value": 1}, {"value": 2}])

    def test_get_all_events_for_key_out_of_order_inserts(self):
        tbes = TimeBaseEventStore()
        tbes.add("key", 1, {"value": 1})
        tbes.add("key", 2, {"value": 2})
        tbes.add("key", 0, {"value": 0})
        self.assertEqual(tbes.get_all("key"), [{"value": 0}, {"value": 1}, {"value": 2}])

    def test_get_first_event_for_key(self):
        tbes = TimeBaseEventStore()
        tbes.add("key", 1, {"value": 1})
        tbes.add("key", 2, {"value": 2})
        self.assertEqual(tbes.get_first("key"), {"value": 1})
