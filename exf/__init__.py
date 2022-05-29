"""Initialize Module."""
from dotenv import load_dotenv
from loguru import logger

logger.disable(__name__)
load_dotenv()

from .main import EXF, read_exf, read_json  # pylint: disable=wrong-import-position # noqa
