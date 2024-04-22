from abc import ABC
from app.repository_orm.base import ORMSessionMixin
from surrealdb import Surreal
sdb = Surreal("http://localhost:9000")
# await sdb.connect()
# await sdb.signin({"user": "root", "pass": "root"})
# await sdb.use("rtcs", "rtcs")

def objects_to_dicts(object_list):
    return [item.__dict__ for item in object_list]

def dicts_to_objects(dict_list, object_class):
    return [object_class(**item) for item in dict_list]

class IRepository(ABC):
    async def create(self, *args, **kwargs):
        raise NotImplemented()

    async def list(self, *args):
        raise NotImplemented()

    async def get(self, *args, id_):
        raise NotImplemented()

    async def update(self, *args, **fields):
        raise NotImplemented()

    async def delete(self, *args, id_):
        raise NotImplemented()


class SurrealORM(IRepository):
    async def create(self, *args, **kwargs):
        table=args[0]().__class__.__name__
        data = kwargs if args[1]==None else args[1].__dict__
        return args[0](**((await sdb.create(table,data))[0]))

    async def list(self, *args):
        table=args[0]().__class__.__name__
        return dicts_to_objects(await sdb.select(table),args[0])

    async def get(self, *args, id_):
        table=args[0]().__class__.__name__
        sql = f"select * from {table} where id = {_id}"
        return args[0](**((await sdb.query(sql))[0]['result'][0]))

    async def update(self, *args, **fields):
        table=args[0]().__class__.__name__
        data = fields if args[1]==None else args[1].__dict__
        return args[0](**((await sdb.update(table,data))[0]))

    async def delete(self, *args, id_):
        table=args[0]().__class__.__name__
        raise NotImplemented()

class PostGresORM(IRepository):
    async def create(self, *args, **kwargs):
        """This method creates a new user."""
        model=args[0]
        data = kwargs if args[1]==None else args[1].__dict__
        user = model(**data)
        self.orm.add(user)
        self.orm.commit()
        self.orm.refresh(user)
        return user
        

    async def list(self, *args):
        model=args[0]
        return self.orm.query(model)

    async def get(self, *args, id_):
        raise NotImplemented()

    async def update(self, *args, **fields):
        raise NotImplemented()

    async def delete(self, *args, id_):
        raise NotImplemented()
