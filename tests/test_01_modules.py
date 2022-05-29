"""Run module tests."""
import pytest
IN_FILE = 'tests/test1.exf'


@pytest.mark.test_modules
def test_read():
    """Test main package works."""
    import exf  # pylint: disable=import-outside-toplevel, unused-import
    exf.read_exf('tests/test1.exf')
    assert True


@pytest.mark.test_modules
def test_exf():
    """Test main package works."""
    import exf  # pylint: disable=import-outside-toplevel, unused-import
    record = exf.read_exf('tests/test1.exf')
    assert record.file_version.major == 1
    record.to_exf()
    record.to_json()
    assert True


@pytest.mark.test_modules
def test_json():
    """Test main package works."""
    import exf  # pylint: disable=import-outside-toplevel, unused-import
    record = exf.read_exf('tests/test1.exf')
    assert record.file_version.major == 1
    record.to_exf()
    record.to_json()
    assert True
