from app.controllers.controller import rc
from app.utils.tools import tools

_list = []
_index = {}


def _get_fake_data():
    return {
        "id": tools.generate_request_id(),
        "content": "hello world",
    }


@rc
async def query_list():
    return _list


@rc
async def add_list():
    row = _get_fake_data()
    _list.append(row)
    _index[row["id"]] = len(_list)
    return row


@rc
async def delete_list(id):
    index = _index[id]
    return _list.pop(index)


@rc
def raise_list():
    raise NotImplementedError
