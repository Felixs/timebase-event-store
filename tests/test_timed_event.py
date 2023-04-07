import unittest
from unittest.mock import patch

from event_store.timed_event import TimedEvent


class TestTimedEvent(unittest.TestCase):
    def test_timed_event(self):
        te = TimedEvent(0, {})
        self.assertIsInstance(te, TimedEvent)

    def test_timestamp(self):
        te = TimedEvent(0, {})
        self.assertEqual(te.timestamp, 0)

    def test_data(self):
        te = TimedEvent(0, {})
        self.assertEqual(te.data, {})

    @patch("time.time_ns")
    def test_created_at(self, mock_time):
        mock_time.return_value = 1
        te = TimedEvent(0, {})
        self.assertEqual(te.created_at, 1)

    @patch("time.time_ns")
    def test_eq(self, mock_time):
        mock_time.return_value = 0
        te1 = TimedEvent(0, {})
        te2 = TimedEvent(0, {})
        self.assertEqual(te1, te2)

    @patch("time.time_ns")
    def test_ne_timestamp(self, mock_time):
        mock_time.return_value = 0
        te1 = TimedEvent(0, {})
        te2 = TimedEvent(1, {})
        self.assertNotEqual(te1, te2)

    @patch("time.time_ns")
    def test_ne_data(self, mock_time):
        mock_time.return_value = 0
        te1 = TimedEvent(0, {})
        te2 = TimedEvent(0, {"a": 1})
        self.assertNotEqual(te1, te2)

    def test_sort_event_list(self):
        te1 = TimedEvent(0, {})
        te2 = TimedEvent(1, {})
        te3 = TimedEvent(2, {})
        event_list = [te3, te2, te1]
        event_list.sort()
        self.assertEqual(event_list, [te1, te2, te3])

    def test_sort_event_list_by_creation(self):
        te1 = TimedEvent(0, {})
        te2 = TimedEvent(0, {})
        te3 = TimedEvent(0, {})
        event_list = [te3, te2, te1]
        event_list.sort()
        self.assertEqual(event_list, [te1, te2, te3])
