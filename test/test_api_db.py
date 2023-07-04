import random
import string
from unittest import TestCase

from app.core import api_db
from app.models import schema


def generate_user_data() -> dict:
    """Generate random user data."""
    username = "user_" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    status = random.choice(["active", "inactive", "suspended"])
    return {"username": username, "status": status}


class Test(TestCase):
    table = schema.Mxuser

    def test_insert_one(self):
        data1 = generate_user_data()
        data2 = generate_user_data()

        ok = api_db.insert(self.table, data=data1)
        assert ok == "ok"
        instance = api_db.insert(self.table, data=data2, refresh=True)
        assert instance.status == data2["status"] and instance.username == data2["username"]

    def test_insert_many(self):
        data1 = [generate_user_data() for _ in range(5)]
        data2 = [generate_user_data() for _ in range(5)]

        ok = api_db.insert(self.table, data=data1)
        assert ok == "ok"
        instances = api_db.insert(self.table, data=data2, refresh=True)
        result = [
            {"status": instance.status, "username": instance.username}
            for instance in instances
        ]

        assert all(item in result for item in data2) and all(
            item in data2 for item in result
        )

    def test_delete_one(self):
        _id1 = 77
        _id2 = 82
        ok = api_db.delete(self.table, id=_id1)
        assert ok == "ok"

    def test_delete_many(self):
        _id1 = [89, 90]
        _id2 = [91, 92]
        ok = api_db.delete(self.table, id=_id1)
        assert ok == "ok"

    def test_update_one(self):
        api_db.update(self.table,id=)

    def test_update_many(self):
        self.fail()

    def test_upsert(self):
        self.fail()
