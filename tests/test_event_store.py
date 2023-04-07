import unittest

from event_store import EventStore


class TestEventStore(unittest.TestCase):
    def test_event_store(self):
        es = EventStore()
        self.assertIsInstance(es, EventStore)

    def test_event_store_add_event(self):
        es = EventStore()
        es.add("key", {"test": 1})
        self.assertEqual(es.get("key"), {"test": 1})

    def test_event_store_get_latest_key_version(self):
        es = EventStore()
        es.add("key", {"test": 1})
        self.assertEqual(es._get_latest_key_version("key"), 0)
        es.add("key", {"test": 2})
        self.assertEqual(es._get_latest_key_version("key"), 1)

    def test_event_store_get_latest_key_version_unknown_key(self):
        es = EventStore()
        self.assertEqual(es._get_latest_key_version("key"), -1)

    def test_event_store_get_next_key_version(self):
        es = EventStore()
        es.add("key", {"test": 1})
        self.assertEqual(es._get_next_key_version("key"), 1)
        es.add("key", {"test": 2})
        self.assertEqual(es._get_next_key_version("key"), 2)

    def test_event_store_add_event_multiple(self):
        es = EventStore()
        es.add("key", {"test": 1})
        self.assertEqual(es.get("key"), {"test": 1})
        es.add("key", {"test": 2})
        self.assertEqual(es.get("key"), {"test": 2})

    def test_event_store_get_latest_event(self):
        es = EventStore()
        es.add("key", {"test": 1})
        es.add("key", {"test": 2})
        self.assertEqual(es.get("key"), {"test": 2})

    def test_event_store_get_unknown_key(self):
        es = EventStore()
        self.assertEqual(es.get("key"), {})

    def test_event_store_get_all_events_for_key(self):
        es = EventStore()
        es.add("key", {"test": 1})
        es.add("key", {"test": 2})
        self.assertEqual(es.get_all("key"), [{"test": 1}, {"test": 2}])

    def test_event_store_get_all_events_for_unknown_key(self):
        es = EventStore()
        self.assertEqual(es.get_all("key"), [])

    def test_event_store_delete_events_by_key(self):
        es = EventStore()
        es.add("key", {"test": 1})
        es.delete("key")
        self.assertEqual(es.get_all("key"), [])

    def test_event_store_delete_existing_key(self):
        es = EventStore()
        es.add("key", {"test": 1})
        self.assertEqual(es.delete("key"), True)

    def test_event_store_delete_missing_key(self):
        es = EventStore()
        self.assertEqual(es.delete("key"), False)

    def test_event_store_get_version(self):
        es = EventStore()
        es.add("key", {"test": 1})
        self.assertEqual(es.get_version("key", 0), {"test": 1})
        es.add("key", {"test": 2})
        self.assertEqual(es.get_version("key", 1), {"test": 2})
        es.add("key", {"test": 3})
        self.assertEqual(es.get_version("key", 2), {"test": 3})

    def test_event_store_get_version_unknown_key(self):
        es = EventStore()
        self.assertEqual(es.get_version("key", 0), {})

    def test_event_store_get_keys(self):
        es = EventStore()
        es.add("key1", {"test": 1})
        es.add("key2", {"test": 2})
        self.assertEqual(es.keys(), ["key1", "key2"])

    def test_event_store_get_keys_empty(self):
        es = EventStore()
        self.assertEqual(es.keys(), [])

    def test_event_store_get_keys_after_delete(self):
        es = EventStore()
        es.add("key1", {"test": 1})
        es.add("key2", {"test": 2})
        es.delete("key1")
        self.assertEqual(es.keys(), ["key2"])

    def test_event_store_get_keys_after_delete_unknown_key(self):
        es = EventStore()
        es.add("key1", {"test": 1})
        es.add("key2", {"test": 2})
        es.delete("key3")
        self.assertEqual(es.keys(), ["key1", "key2"])

    def test_event_store_get_all_format(self):
        es = EventStore()
        es.add("key1", {"test": 1, "value": 2})
        es.add("key1", {"test": 2, "value": 3})
        es.add("key1", {"test": 2, "value": 4})
        result = es.get_all_format("key1", {"value": int})
        self.assertEqual(result, [{"value": 2}, {"value": 3}, {"value": 4}])

    def test_event_store_get_all_format_wrong_type(self):
        es = EventStore()
        es.add("key1", {"test": 1, "value": 2})
        es.add("key1", {"test": 2, "value": "hello"})
        es.add("key1", {"test": 2, "value": 4})
        result = es.get_all_format("key1", {"value": int})
        self.assertEqual(result, [{"value": 2}, {"value": None}, {"value": 4}])

    def test_event_store_get_all_format_missing_data(self):
        es = EventStore()
        es.add("key1", {"test": 1, "value": 2})
        es.add("key1", {"test": 2})
        es.add("key1", {"test": 2, "value": 4})
        result = es.get_all_format("key1", {"value": int})
        self.assertEqual(result, [{"value": 2}, {"value": None}, {"value": 4}])
