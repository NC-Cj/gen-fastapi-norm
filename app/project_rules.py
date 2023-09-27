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
    OUTPUT_UNHANDLED_EXCEPTIONS = True
    LOGGING_CUSTOM_RESPONSE_CODE = False
    LOGGING_ALL_REQUESTS = False
    LOGGING_NON_200_STATUS = False


class ResponseCode:
    SUCCESS = 1000
    FAILURE = 1001
    INTERNAL_ERROR = 1002


GlobalProjectResponses = {
    200: {
        "description": "Successful response",
        "model": PublicResponse,
        "content": {
            "application/json": {
                "examples": {
                    "example1": {
                        "summary": "success example",
                        "value": PublicResponse(
                            code=ResponseCode.SUCCESS,
                            data=[],
                            msg="success"
                        )
                    },
                    "example2": {
                        "summary": "error example",
                        "value": PublicResponse(
                            code=ResponseCode.FAILURE,
                            data=None,
                            msg="{error message}"
                        )
                    },
                    "example3": {
                        "summary": "internal error example",
                        "value": PublicResponse(
                            code=ResponseCode.INTERNAL_ERROR,
                            data=None,
                            msg="service busy or {error stack}"
                        )
                    }
                }
            }
        }
    }
}
