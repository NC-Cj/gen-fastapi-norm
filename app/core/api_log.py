import sys

from loguru import logger

logger.remove()

logger.configure(
    handlers=[
        dict(
            # Refer to: https://loguru.readthedocs.io/en/stable/overview.html
            # And customize it
            sink=sys.stdout,
            colorize=True,
            format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
        )
    ]
)


def __test_log_output():
    content = "Something went wrong"

    logger.error(content)
    logger.info(content)
    logger.debug(content)
    logger.warning(content)
    logger.success(content)
    logger.trace(content)
    logger.critical(content)

# test_log_output()
