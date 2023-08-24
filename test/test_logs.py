from app.core.logger.log_setup import logger


def __test_log_output():
    content = "Something went wrong"

    logger.error(content)
    logger.info(content)
    logger.debug(content)
    logger.warning(content)
    logger.success(content)
    logger.trace(content)
    logger.critical(content)


__test_log_output()
