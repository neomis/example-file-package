"""Click interface."""
import sys
import click
from loguru import logger
from .config import ENVIRONMENT


logger.enable(__package__)
logger.remove(0)


@click.command()
@click.argument('file_path', type=str)
@click.argument('out_path', type=str, required=False)
@click.option('--loglevel', 'log_level', type=click.Choice(['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'], case_sensitive=False), default='ERROR')
@click.version_option()
def exf_to_json(file_path, out_path, log_level) -> None:
    """Convert EXF to JSON"""
    import exf  # pylint: disable=import-outside-toplevel
    logger.add(sys.stderr, colorize=True, level=log_level)
    logger.info(f"ENVIRONMENT: {ENVIRONMENT}")
    logger.info(f"LOG LEVEL: {log_level}")
    record = exf.read_exf(file_path)
    out = record.to_json(out_path)
    if out is not None:
        click.echo(out)


@click.command()
@click.argument('file_path', type=str)
@click.argument('out_path', type=str, required=False)
@click.option('--loglevel', 'log_level', type=click.Choice(['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'], case_sensitive=False), default='ERROR')
@click.version_option()
def json_to_exf(file_path, out_path, log_level) -> None:
    """Convert EXF to JSON"""
    import exf  # pylint: disable=import-outside-toplevel
    logger.add(sys.stderr, colorize=True, level=log_level)
    logger.info(f"ENVIRONMENT: {ENVIRONMENT}")
    logger.info(f"LOG LEVEL: {log_level}")
    record = exf.read_json(file_path)
    out = record.to_exf(out_path)
    if out is not None:
        click.echo(out)
