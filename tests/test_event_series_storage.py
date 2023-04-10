import unittest

from event_series import EventSeries, EventSeriesStorage


class TestEventSeriesStorage(unittest.TestCase):
    def test_init(self):
        ess = EventSeriesStorage()
        self.assertIsInstance(ess, EventSeriesStorage)

    def test_add(self):
        ess = EventSeriesStorage()
        ess.add("key", 1, {"test": 1})
        self.assertIsInstance(ess._data["key"], EventSeries)

    def test_get_values(self):
        ess = EventSeriesStorage()
        ess.add("key", 1, {"test": 1})
        self.assertEqual(ess.key_value_series("key", "test"), [(1, 1)])

    def test_get_values_for_missing_key(self):
        ess = EventSeriesStorage()
        self.assertRaises(KeyError, ess.key_value_series, "key", "test")

    def test_get_values_for_missing_value(self):
        ess = EventSeriesStorage()
        ess.add("key", 1, {"test": 1})
        self.assertEqual(ess.key_value_series("key", ""), [])

    def test_clear(self):
        ess = EventSeriesStorage()
        ess.add("key", 1, {"test": 1})
        ess.clear()
        self.assertEqual(len(ess._data), 0)

    def test_get_keys(self):
        ess = EventSeriesStorage()
        ess.add("key", 1, {"test": 1})
        self.assertEqual(ess.keys(), ["key"])
        ess.add("key2", 1, {"test": 1})
        self.assertEqual(ess.keys(), ["key", "key2"])

    def test_get_keys_for_missing_key(self):
        ess = EventSeriesStorage()
        self.assertEqual(ess.keys(), [])

    def test_get_value_series(self):
        ess = EventSeriesStorage()
        ess.add("key", 1, {"test": 1})
        ess.add("key2", 2, {"test": 2})
        self.assertEqual(ess.value_series("test"), {"key": [(1, 1)], "key2": [(2, 2)]})

    def test_get_value_series_for_part_of_series(self):
        ess = EventSeriesStorage()
        ess.add("key", 1, {"test": 1})
        ess.add("key2", 2, {"test2": 2})
        self.assertEqual(ess.value_series("test2"), {"key2": [(2, 2)]})

    def test_get_value_series_for_missing_value(self):
        ess = EventSeriesStorage()
        ess.add("key", 1, {"test": 1})
        ess.add("key2", 2, {"test": 2})
        self.assertRaises(KeyError, ess.value_series, "test3")
