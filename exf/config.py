"""Environment Config."""
import os
ENVIRONMENT: str = os.getenv("ENVIRONMENT", "PRODUCTION")
ENCODING: str = os.getenv("ENCODING", "UTF-8")
