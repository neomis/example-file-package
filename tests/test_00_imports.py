"""Test Importing the package works."""
import pytest


@pytest.mark.test_package
def test_import():
    """Test imporint package works."""
    from python_template.main import main  # pylint: disable=import-outside-toplevel, unused-import
    assert True
