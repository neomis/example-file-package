"""Environment Config."""
import os
from tarfile import ENCODING
ENVIRONMENT: str = os.getenv("ENVIRONMENT", "PRODUCTION")
ENCODING: str = os.getenv("ENCODING", "UTF-8")
