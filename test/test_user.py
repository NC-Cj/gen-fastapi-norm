from unittest import TestCase

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


class Test(TestCase):
    def test_query_user_list(self):
        pass

    def test_query_user(self):
        pass
