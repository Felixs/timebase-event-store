import unittest

from event_series import EventSeries


class TestEventSeries(unittest.TestCase):
    def test_event_series_init(self):
        es = EventSeries()
        self.assertIsInstance(es, EventSeries)

    def test_single_insert(self):
        es = EventSeries()
        es.add(1, {"a": 1})
        self.assertEqual(es.get("a"), [(1, 1)])

    def test_multiple_insert(self):
        es = EventSeries()
        es.add(1, {"a": 1})
        es.add(2, {"a": 2})
        self.assertEqual(es.get("a"), [(1, 1), (2, 2)])

    def test_single_multiple_keys(self):
        es = EventSeries()
        es.add(1, {"a": 1, "b": 2})
        self.assertEqual(es.get("a"), [(1, 1)])
        self.assertEqual(es.get("b"), [(1, 2)])

    def test_multiple_multiple_keys(self):
        es = EventSeries()
        es.add(1, {"a": 1, "b": 2})
        es.add(2, {"a": 3, "b": 4})
        self.assertEqual(es.get("a"), [(1, 1), (2, 3)])
        self.assertEqual(es.get("b"), [(1, 2), (2, 4)])

    def test_multiple_keys_missing(self):
        es = EventSeries()
        es.add(1, {"a": 1})
        es.add(2, {"b": 4})
        self.assertEqual(es.get("a"), [(1, 1)])
        self.assertEqual(es.get("b"), [(2, 4)])

    def test_insert_multiple_out_of_order(self):
        es = EventSeries()
        es.add(2, {"a": 1})
        es.add(1, {"a": 2})
        self.assertEqual(es.get("a"), [(1, 2), (2, 1)])

    def test_missing_key(self):
        es = EventSeries()
        self.assertEqual(es.get("a"), [])

    def test_get_keys(self):
        es = EventSeries()
        es.add(1, {"a": 1, "b": 2})
        self.assertEqual(es.get_keys(), {"a", "b"})

    def test_get_keys_empty(self):
        es = EventSeries()
        self.assertEqual(es.get_keys(), set())

    def test_get_keys_after_get_missing_key(self):
        es = EventSeries()
        es.get("a")
        self.assertEqual(es.get_keys(), set())

    def test_add_multi_level_dict(self):
        es = EventSeries()
        es.add(1, {"a": {"b": 1}})
        self.assertEqual(es.get("a.b"), [(1, 1)])
        self.assertEqual(es.get("a"), [])
        self.assertEqual(es.get_keys(), {"a.b"})

    def test_add_multiple_with_same_timestamp(self):
        es = EventSeries()
        es.add(1, {"a": 1})
        es.add(1, {"a": 2})
        self.assertEqual(es.get("a"), [(1, 1), (1, 2)])

    def test_clear(self):
        es = EventSeries()
        es.add(1, {"a": 1})
        self.assertEqual(es.get("a"), [(1, 1)])
        es.clear()
        self.assertEqual(es.get("a"), [])
