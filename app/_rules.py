class Rule:
    # The exception thrown in the program will print the error stack
    PRINT_ERROR_STACK = False
    # Uncaptured service internal exception will be returned in the response
    OUTPUT_INTERNAL_ERROR = True
    # Add request headers middleware
    ADD_LINK_TRACKING_MIDDLEWARE = True
    # Add request logging middleware
    ADD_REQUEST_LOGGING_MIDDLEWARE = True


class ResponseCode:
    SUCCESS = 1000
    FAILURE = 1001
    INTERNAL_ERROR = 1002
