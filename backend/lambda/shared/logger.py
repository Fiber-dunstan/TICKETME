"""
Shared structured logging setup for all TicketMe Lambda functions.
CloudWatch automatically captures anything printed via the logging module,
so consistent, leveled logging here gives us real observability later.
"""
import logging
import os


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(os.environ.get("LOG_LEVEL", "INFO"))
    return logger