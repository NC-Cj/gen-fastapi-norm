from ..core import api_db
from ..models.schema import Domain, Fn


# def query_user_list():
#     return api_db.query_all(Mxuser)
#
#
# def query_user(uid):
#     return api_db.query_first(Mxuser, id=uid)
#
#
# def insert_user(model):
#     return api_db.insert(Mxuser, data=model, refresh=True)
#
#
# #
# # def insert_users(model: List[request.User]):
# #     return api_db.insert(Mxuser, data=model, refresh=True)
#
#
# def update_user(uid, status):
#     return api_db.upsert(Mxuser, data=[])


def query_domain_list():
    return api_db.query(
        Domain,
        joins=[Domain.fn],
        includes=['Fn']
    )
