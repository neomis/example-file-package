"""Main program."""
import arrow
from loguru import logger


def main(**kwargs) -> None:
    """Execute main function."""
    start_date = arrow.now().to('local')
    logger.info("Main Program Started.")
    logger.debug(f"START_DATE: {start_date}")
    for key, value in kwargs.items():
        logger.debug(f"{key}: {value}")
    print("Hello World.")
