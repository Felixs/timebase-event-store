import unittest
from event_store.timed_event import TimedEvent

from event_store.timed_event_series import TimedEventSeries


class TestTimedEventSeries(unittest.TestCase):
    def test_init(self):
        tes = TimedEventSeries()
        self.assertIsInstance(tes, TimedEventSeries)

    def test_data(self):
        tes = TimedEventSeries()
        self.assertEqual(tes.data, [])

    def test_add_event(self):
        tes = TimedEventSeries()
        event = TimedEvent(1, {"test": "test"})
        tes.add(event)
        self.assertEqual(tes.data, [event])

    def test_get_event(self):
        tes = TimedEventSeries()
        event = TimedEvent(1, {"test": "test"})
        tes.add(event)
        self.assertEqual(tes.get(), event)

    def test_get_event_latest(self):
        tes = TimedEventSeries()
        event = TimedEvent(1, {"test": "test"})
        tes.add(event)
        event2 = TimedEvent(2, {"test": "test2"})
        tes.add(event2)
        self.assertEqual(tes.get(), event2)

    def test_get_event_latest_out_of_order_add(self):
        tes = TimedEventSeries()
        event2 = TimedEvent(2, {"test": "test2"})
        tes.add(event2)
        event = TimedEvent(1, {"test": "test"})
        tes.add(event)
        self.assertEqual(tes.get(), event2)

    def test_get_all_events(self):
        tes = TimedEventSeries()
        event = TimedEvent(1, {"test": "test"})
        tes.add(event)
        event2 = TimedEvent(2, {"test": "test2"})
        tes.add(event2)
        event3 = TimedEvent(3, {"test": "test3"})
        tes.add(event3)
        self.assertEqual(tes.get_all(), [event, event2, event3])

    def test_get_first_event(self):
        tes = TimedEventSeries()
        event = TimedEvent(1, {"test": "test"})
        tes.add(event)
        event2 = TimedEvent(2, {"test": "test2"})
        tes.add(event2)
        self.assertEqual(tes.get_first(), event)

    def test_get_all_transitions(self):
        tes = TimedEventSeries()
        event = TimedEvent(1, {"test": "test"})
        tes.add(event)
        event2 = TimedEvent(2, {"test": "test2"})
        tes.add(event2)
        changes = {"test": ["test", "test2"]}
        self.assertEqual(tes.get_all_transitions(), changes)

    def test_get_all_transitions_multiple(self):
        tes = TimedEventSeries()
        event = TimedEvent(1, {"test": "test", "value": 1})
        tes.add(event)
        event2 = TimedEvent(2, {"test": "test2", "value": 2})
        tes.add(event2)
        changes = {"test": ["test", "test2"], "value": [1, 2]}
        self.assertEqual(tes.get_all_transitions(), changes)

    def test_get_all_transitions_missing_key(self):
        tes = TimedEventSeries()
        event = TimedEvent(1, {"test": "test"})
        tes.add(event)
        event2 = TimedEvent(2, {})
        tes.add(event2)
        event3 = TimedEvent(2, {"test": "test2"})
        tes.add(event3)
        changes = {"test": ["test", "test2"]}
        self.assertEqual(tes.get_all_transitions(), changes)

    def test_get_transition(self):
        tes = TimedEventSeries()
        event = TimedEvent(1, {"test": "test"})
        tes.add(event)
        event2 = TimedEvent(2, {"test": "test2"})
        tes.add(event2)
        changes = ["test", "test2"]
        self.assertEqual(tes.get_transition("test"), changes)

    def test_get_version(self):
        tes = TimedEventSeries()
        event = TimedEvent(1, {"test": "test"})
        tes.add(event)
        event2 = TimedEvent(2, {"test": "test2"})
        tes.add(event2)
        self.assertEqual(tes.version, 2)

    def test_get_version_empty(self):
        tes = TimedEventSeries()
        self.assertEqual(tes.version, 0)

    def test_get_version_out_of_order(self):
        tes = TimedEventSeries()
        event2 = TimedEvent(2, {"test": "test2"})
        tes.add(event2)
        event = TimedEvent(1, {"test": "test"})
        tes.add(event)
        self.assertEqual(tes.version, 2)

    def test_contains(self):
        tes = TimedEventSeries()
        event = TimedEvent(1, {"test": "test"})
        tes.add(event)
        event2 = TimedEvent(2, {"test": "test2"})
        tes.add(event2)
        self.assertTrue(tes.contains("test", "test2"))

    def test_contains_not(self):
        tes = TimedEventSeries()
        event = TimedEvent(1, {"test": "test"})
        tes.add(event)
        event2 = TimedEvent(2, {"test": "test2"})
        tes.add(event2)
        self.assertFalse(tes.contains("test", "test3"))

    def test_contains_not_key(self):
        tes = TimedEventSeries()
        event = TimedEvent(1, {"test": "test"})
        tes.add(event)
        event2 = TimedEvent(2, {"test": "test2"})
        tes.add(event2)
        self.assertFalse(tes.contains("unknown", "test3"))

    def test_to_time_series(self):
        tes = TimedEventSeries()
        event = TimedEvent(1, {"test": "test"})
        tes.add(event)
        event2 = TimedEvent(2, {"test": "test2"})
        tes.add(event2)
        ts = tes.to_time_series({"test": str})
        self.assertEqual(ts, [("test",), ("test2",)])

    def test_to_time_series_multiple(self):
        tes = TimedEventSeries()
        event = TimedEvent(1, {"test": "test", "value": 1})
        tes.add(event)
        event2 = TimedEvent(2, {"test": "test2", "value": 1})
        tes.add(event2)
        ts = tes.to_time_series({"test": str, "value": int})
        self.assertEqual(ts, [("test", 1), ("test2", 1)])

    # def test_changes_to(self):
    #     tes = TimedEventSeries()
    #     event = TimedEvent(1, {"test": "test"})
    #     tes.add(event)
    #     event2 = TimedEvent(2, {"test": "test2"})
    #     tes.add(event2)
    #     self.assertEqual(tes.changes_to("test", "test"), ["test2"])
