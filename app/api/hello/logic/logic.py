from app.controllers.controller import serialize


class HelloController:

    def __init__(self, req):
        self.req = req

    @serialize
    async def hello(self, name):
        return f"Hello {name}"
