from app.dao.postgresql import get_session


def query_all(entities, **filters):
    s = get_session()()
    query = s.query(entities).filter(**filters)
    s.close()
    return query.all()

# def query_first(entities, s: Session = Depends(get_session), **filters):
#     query = s.query(entities).filter_by(**filters)
#     return query.first()
#
#
# def insert_many(entities, data: List[dict], s: Session = Depends(get_session)):
#     objs = [entities(**item) for item in data]
#     s.bulk_save_objects(objs)
#     s.commit()
#     s.refresh(objs)
#
#
# def insert_one(entities, data: dict, s: Session = Depends(get_session)):
#     obj = entities(**data)
#     s.add(obj)
#     s.commit()
#     s.refresh(obj)
#     return obj
