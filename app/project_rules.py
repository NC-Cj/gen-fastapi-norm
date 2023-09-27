"""
:example:
    @production:
        class Rule:
            PRINT_ERROR_STACK = True
            OUTPUT_UNHANDLED_EXCEPTIONS = False
            LOGGING_CUSTOM_RESPONSE_CODE = False
            LOGGING_ALL_REQUESTS = False
            LOGGING_NON_200_STATUS = False

    @develop:
        class Rule:
            PRINT_ERROR_STACK = True
            OUTPUT_UNHANDLED_EXCEPTIONS = True
            LOGGING_CUSTOM_RESPONSE_CODE = False
            LOGGING_ALL_REQUESTS = False
            LOGGING_NON_200_STATUS = True
"""


class Rule:
    PRINT_ERROR_STACK = True
    OUTPUT_UNHANDLED_EXCEPTIONS = True
    LOGGING_CUSTOM_RESPONSE_CODE = False
    LOGGING_ALL_REQUESTS = False
    LOGGING_NON_200_STATUS = False


class ResponseCode:
    SUCCESS = 1000
    FAILURE = 1001
    INTERNAL_ERROR = 1002
