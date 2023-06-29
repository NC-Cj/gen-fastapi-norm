class NoPermissions(Exception):
    def __init__(self, message):
        self.message = message


class DatabaseFailure(Exception):
    def __init__(self, message):
        self.message = message


exceptions_to_catch = [NoPermissions, DatabaseFailure]
