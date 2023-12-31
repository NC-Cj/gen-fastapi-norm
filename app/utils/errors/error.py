from fastapi import HTTPException, status


class DatabaseException(Exception):
    def __init__(self,
                 message):
        self.message = message


class CustomHTTPException(HTTPException):
    def __init__(self,
                 message: str,
                 status_code: int = status.HTTP_200_OK):
        self.message = message
        self.status_code = status_code
        super().__init__(status_code=status_code, detail=message)


global_exceptions_to_catch = [DatabaseException]
