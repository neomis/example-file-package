"""Environment Config."""
import os
ENVIRONMENT: str = os.getenv("ENVIRONMENT", "PRODUCTION")
