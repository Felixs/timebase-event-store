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
