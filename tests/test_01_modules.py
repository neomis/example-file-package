"""Run module tests."""
import pytest


@pytest.mark.test_modules
def test_config():
    """Test config file."""
    from exf.config import ENVIRONMENT  # pylint: disable=import-outside-toplevel, unused-import
    assert isinstance(ENVIRONMENT, str)
    assert ENVIRONMENT in ['PRODUCTION', 'DEVELOPMENT']


@pytest.mark.test_modules
def test_main():
    """Test main package works."""
    from exf.main import main  # pylint: disable=import-outside-toplevel, unused-import
    main()
    assert True
