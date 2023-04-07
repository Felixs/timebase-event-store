import unittest
from unittest.mock import patch
from event_store.event import Event


class TestEvent(unittest.TestCase):
    def test_event(self):
        e = Event()
        self.assertIsInstance(e, Event)

    def test_event_init(self):
        e = Event()
        self.assertEqual(e.data, {})

    def test_event_ttl(self):
        e = Event(ttl=0)
        self.assertEqual(e.ttl, 0)

    def test_event_missing_ttl(self):
        e = Event()
        self.assertEqual(e.ttl, -1)

    def test_event_data(self):
        e = Event(data={"test": 1})
        self.assertEqual(e.data, {"test": 1})

    def test_event_expires_at(self):
        e = Event(expires_at=1)
        self.assertEqual(e.expires_at, 1)

    @patch("time.time")
    def test_event_expires_at_expires(self, mock_time):
        e = Event(expires_at=1)
        mock_time.return_value = 2.0
        self.assertTrue(e.expired)

    @patch("time.time")
    def test_event_timestamp(self, mock_time):
        mock_time.return_value = 1.0
        e = Event()
        self.assertEqual(e.timestamp, 1.0)

    @patch("time.time")
    def test_event_invalid(self, mock_time):
        mock_time.return_value = 0.0
        e = Event(ttl=100)
        mock_time.return_value = 101.0
        self.assertTrue(e.expired)

    @patch("time.time")
    def test_event_valid_in_ttl(self, mock_time):
        mock_time.return_value = 0.0
        e = Event(ttl=100)
        mock_time.return_value = 100.0
        self.assertFalse(e.expired)

    @patch("time.time")
    def test_event_without_ttl_allways_valid(self, mock_time):
        mock_time.return_value = 0.0
        e = Event()
        mock_time.return_value = 100000.0
        self.assertFalse(e.expired)

    def test_event_formated_data(self):
        e = Event(data={"test": 1, "value": 2})
        self.assertEqual(e.formated_data({"value": int}), {"value": 2})

    def test_event_formated_data_missing(self):
        e = Event(data={"test": 1})
        self.assertEqual(e.formated_data({"value": int}), {"value": None})

    def test_event_formated_data_wrong_type(self):
        e = Event(data={"test": "test"})
        self.assertEqual(e.formated_data({"value": int}), {"value": None})
