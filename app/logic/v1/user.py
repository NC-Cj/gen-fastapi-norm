from ...controllers.controllers import catch_controller
from ...dao import crud


@catch_controller
def query_user_list():
    return crud.query_user_list()
