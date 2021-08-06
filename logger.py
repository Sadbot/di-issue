import logging
import sys

import orjson
from loguru import logger

LOG_LEVEL_MAPPING = {
    "sqlalchemy.log": "WARNING",
}


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1
        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def init_logger(log_level: str):
    logger.remove()
    seen = set()
    for name in [
        *logging.root.manager.loggerDict.keys(),
        "gunicorn",
        "gunicorn.access",
        "gunicorn.error",
        "uvicorn",
        "uvicorn.access",
        "uvicorn.error",
        "fastapi",
    ]:
        if name not in seen:
            seen.add(name.split(".")[0])
            logging.getLogger(name).handlers = [InterceptHandler()]

    logger.configure(handlers=[{"sink": sys.stdout, "serialize": False, "enqueue": True}])
    logger.level(log_level)

    return logger
