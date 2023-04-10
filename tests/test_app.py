import unittest
from httpx import AsyncClient

from api.app import create_app, cleanup


class TestAppMain(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.app = create_app()

    def tearDown(self) -> None:
        cleanup()
        return super().tearDown()

    async def test_get_root(self):
        async with AsyncClient(app=self.app, base_url="http://test") as ac:
            response = await ac.get("/")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), {"message": "Hello World"})

    async def test_add_event(self):
        async with AsyncClient(app=self.app, base_url="http://test") as ac:
            response = await ac.post("/event", json={"timestamp": 1, "data": {"a": 1, "b": 2}})
            self.assertEqual(response.status_code, 200)

    async def test_add_event_without_timestamp(self):
        async with AsyncClient(app=self.app, base_url="http://test") as ac:
            response = await ac.post("/event", json={"data": {"a": 1, "b": 2}})
            self.assertEqual(response.status_code, 200)
            response = await ac.get("/event/a")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["data"][0][1], 1)
            response = await ac.get("/event/b")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["data"][0][1], 2)

    async def test_get_event(self):
        async with AsyncClient(app=self.app, base_url="http://test") as ac:
            await ac.post("/event", json={"timestamp": 1, "data": {"a": 1, "b": 2}})
            response = await ac.get("/event/a")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), {"data": [[1, 1]]})

    async def test_get_multiple_event(self):
        async with AsyncClient(app=self.app, base_url="http://test") as ac:
            await ac.post("/event", json={"timestamp": 1, "data": {"a": 1, "b": 2}})
            await ac.post("/event", json={"timestamp": 2, "data": {"a": 1, "b": 3}})
            await ac.post("/event", json={"timestamp": 3, "data": {"a": 1, "b": 4}})
            response = await ac.get("/event/a")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), {"data": [[1, 1], [2, 1], [3, 1]]})
            response = await ac.get("/event/b")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), {"data": [[1, 2], [2, 3], [3, 4]]})

    async def test_get_missing_event_key(self):
        async with AsyncClient(app=self.app, base_url="http://test") as ac:
            await ac.post("/event", json={"timestamp": 1, "data": {"a": 1, "b": 2}})
            response = await ac.get("/event/c")
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json(), {"detail": "No data for key"})

    async def test_reset_data(self):
        async with AsyncClient(app=self.app, base_url="http://test") as ac:
            await ac.post("/event", json={"timestamp": 1, "data": {"a": 1, "b": 2}})
            response = await ac.get("/event/a")
            self.assertEqual(response.status_code, 200)
            response = await ac.delete("/reset")
            self.assertEqual(response.status_code, 200)
            response = await ac.get("/event/c")
            self.assertEqual(response.status_code, 404)

    async def test_add_events_by_id(self):
        async with AsyncClient(app=self.app, base_url="http://test") as ac:
            response = await ac.post("/events/1", json={"timestamp": 1, "data": {"a": 1, "b": 2}})
            self.assertEqual(response.status_code, 200)

    async def test_get_events_value_by_id(self):
        async with AsyncClient(app=self.app, base_url="http://test") as ac:
            response = await ac.post("/events/1", json={"timestamp": 1, "data": {"a": 1, "b": 2}})
            self.assertEqual(response.status_code, 200)
            response = await ac.get("/events/1/a")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), {"data": [[1, 1]]})

    async def test_get_events_values_by_id_for_missing_id(self):
        async with AsyncClient(app=self.app, base_url="http://test") as ac:
            response = await ac.get("/values/a")
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json(), {"detail": "No data for value a"})

    async def test_get_events_values_by_id_for_missing_key(self):
        async with AsyncClient(app=self.app, base_url="http://test") as ac:
            response = await ac.post("/events/1", json={"timestamp": 1, "data": {"a": 1, "b": 2}})
            self.assertEqual(response.status_code, 200)
            response = await ac.get("/values/c")
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json(), {"detail": "No data for value c"})

    async def test_larger_event_series(self):
        async with AsyncClient(app=self.app, base_url="http://test") as ac:
            await ac.post("/events/1", json={"timestamp": 1, "data": {"a": 1, "b": 1}})
            await ac.post("/events/1", json={"timestamp": 2, "data": {"a": 2, "b": 2}})
            await ac.post("/events/1", json={"timestamp": 3, "data": {"a": 3, "b": 3}})
            await ac.post("/events/1", json={"timestamp": 4, "data": {"a": 4, "b": 4}})
            await ac.post("/events/1", json={"timestamp": 5, "data": {"a": 5, "b": 5}})
            await ac.post("/events/2", json={"timestamp": 1, "data": {"c": 5, "b": 5}})
            await ac.post("/events/2", json={"timestamp": 2, "data": {"c": 4, "b": 4}})
            await ac.post("/events/2", json={"timestamp": 3, "data": {"c": 3, "b": 3}})
            await ac.post("/events/2", json={"timestamp": 4, "data": {"c": 2, "b": 2}})
            await ac.post("/events/2", json={"timestamp": 5, "data": {"c": 1, "b": 1}})
            response = await ac.get("/values/a")
            self.assertEqual(
                response.json(),
                {
                    "data": {
                        "1": [[1, 1], [2, 2], [3, 3], [4, 4], [5, 5]],
                    }
                },
            )
            response = await ac.get("/values/b")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                response.json(),
                {
                    "data": {
                        "1": [[1, 1], [2, 2], [3, 3], [4, 4], [5, 5]],
                        "2": [[1, 5], [2, 4], [3, 3], [4, 2], [5, 1]],
                    }
                },
            )
            response = await ac.get("/values/c")
            self.assertEqual(
                response.json(),
                {
                    "data": {
                        "2": [[1, 5], [2, 4], [3, 3], [4, 2], [5, 1]],
                    }
                },
            )
