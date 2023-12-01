from app.models.response import PublicResponse

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
    OUTPUT_ERROR_STACK = False
    OUTPUT_UNHANDLED_EXCEPTIONS = True
    LOGGING_CUSTOM_RESPONSE_CODE = False
    LOGGING_ALL_REQUESTS = False
    LOGGING_NON_200_STATUS = False


success_example = None
error_example = None
internal_error_example = None

GlobalProjectResponses = {
    200: {
        "description": "Successful response",
        "model": PublicResponse,
        "content": {
            "application/json": {
                "examples": {
                    "example1": {
                        "summary": "success example",
                        "value": success_example
                    },
                    "example2": {
                        "summary": "error example",
                        "value": error_example
                    },
                    "example3": {
                        "summary": "internal error example",
                        "value": internal_error_example
                    }
                }
            }
        }
    }
}
