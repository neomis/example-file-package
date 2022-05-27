"""Click interface."""
import sys
import click
from loguru import logger
from .config import ENVIRONMENT


logger.enable(__package__)
logger.remove(0)


@click.command()
@click.option('--loglevel', 'log_level', type=click.Choice(['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'], case_sensitive=False), default='ERROR')
@click.version_option()
def cli(log_level) -> None:
    """Main Comand Line Interface"""
    from .main import main  # pylint: disable=import-outside-toplevel
    logger.add(sys.stderr, colorize=True, level=log_level)
    logger.info(f"ENVIRONMENT: {ENVIRONMENT}")
    logger.info(f"LOG LEVEL: {log_level}")
    main()
