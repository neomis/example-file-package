"""Test Shared Utils work."""
from io import StringIO
import pytest
import arrow
import pandas as pd
from loguru import logger
from exf.utils import validate_file, validate_path, read_json, write_json, write_exf


@pytest.mark.test_utils
def test_validation():
    """Test Validate Path and file works."""
    validate_path('tests', 'r')
    validate_path('tests', 'w')
    try:
        validate_path('tests', 'a')
        assert False
    except ValueError as error:
        logger.debug(error)
    try:
        validate_path('/fake!@#path"', 'r')
        assert False
    except ValueError as error:
        logger.debug(error)
    try:
        validate_path('tests/test1.exf', 'r')
        assert False
    except TypeError as error:
        logger.debug(error)

    validate_file('tests/test1.exf', 'r')
    validate_file('tests/test1.exf', 'w')
    try:
        validate_file('tests/test1.exf', 'a')
        assert False
    except ValueError as error:
        logger.debug(error)
    try:
        validate_file('tests')
        assert False
    except TypeError as error:
        logger.debug(error)
    try:
        validate_file('LICENSE', validate_extension=True)
        assert False
    except ValueError as error:
        logger.debug(error)
    try:
        validate_file('not_real')
        assert False
    except ValueError as error:
        logger.debug(error)


@pytest.mark.test_utils
def test_json():
    """Test write_json works."""
    with open('tests/test1.json', 'r') as file_handle:
        data = file_handle.read()
        file_handle.close()
    record = read_json(StringIO(data))
    try:
        data = read_json(None)
        assert False
    except TypeError as error:
        logger.debug(error)
    data = read_json('tests/test1.json')

    data['file_date'] = arrow.get(data['file_date'])
    data['input_config'] = pd.DataFrame(data['input_config'])
    data['data'] = pd.DataFrame(data['data'])
    data['NONE'] = None
    data['NA'] = pd.NA
    write_json(data)
    write_json(data, 'out/out.json')
    write_json(data, 'out/out2')
    try:
        write_json(None)
        assert False
    except ValueError as error:
        logger.debug(error)


@pytest.mark.test_utils
def test_write_exf():
    """Test write_exf works."""
    try:
        write_exf(None)
        assert False
    except ValueError as error:
        logger.debug(error)
