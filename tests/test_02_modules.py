"""Run module tests."""
from io import StringIO
import pytest
import pandas as pd
import arrow
from loguru import logger
IN_FILE = 'tests/test1.exf'


@pytest.mark.test_modules
def test_create():
    """Test EXF class works."""
    from exf import EXF  # pylint: disable=import-outside-toplevel, unused-import
    record = EXF()
    record = EXF(data=pd.DataFrame({'COL1': ["PARAM1", "PARAM2"], 'COL2': [
                 1, 2], 'COL3': [1.4, 1.5], 'COL4': [False, True]}))


@pytest.mark.test_modules
def test_from_string():
    """Test EXF from_string method works."""
    from exf import EXF  # pylint: disable=import-outside-toplevel, unused-import
    try:
        record = EXF.from_string(None)
        assert False
    except ValueError as error:
        logger.debug(error)
    try:
        record = EXF.from_string({})
        assert False
    except TypeError as error:
        logger.debug(error)
    try:
        record = EXF.from_string("")
        assert Fals
    except ValueError as error:
        logger.debug(error)
    try:
        record = EXF.from_string((
            'Example File v1.0\n'
            'FILE_DATE: 2022-05-29\n'
            'TABLE:\nCOL1\nPARAM1\n'
            'END_DATE:2022-05-30\n'))
        assert False
    except ValueError as error:
        logger.debug(error)
    record = EXF.from_string('Example File v1.0\nFILE_DATE: 2022-05-29\n')
    record.to_string()


@pytest.mark.test_modules
def test_from_dict():
    """Test EXF from_dict method works."""
    from exf import EXF  # pylint: disable=import-outside-toplevel, unused-import
    try:
        record = EXF.from_dict(None)
        assert False
    except ValueError as error:
        logger.debug(error)
    try:
        record = EXF.from_dict([])
        assert False
    except TypeError as error:
        logger.debug(error)
    try:
        record = EXF.from_dict({})
        assert Fals
    except ValueError as error:
        logger.debug(error)
    record = EXF.from_dict({'file_version': '1.0'})
    record.to_dict()


@pytest.mark.test_modules
def test_add_parameter():
    """Test EXF add_parameter method works."""
    from exf import EXF  # pylint: disable=import-outside-toplevel, unused-import
    record = EXF()
    record.add_parameter('good_date', '2022-01-01 00:00:00')
    record.add_parameter('good_date', 7)
    try:
        record.add_parameter('bad_date', 1e6000)
        assert False
    except ValueError as error:
        logger.debug(error)
    try:
        record.add_parameter('bad_date', '-')
        assert False
    except ValueError as error:
        logger.debug(error)
    try:
        record.add_parameter(None, '-')
        assert False
    except ValueError as error:
        logger.debug(error)
    try:
        record.add_parameter(9, '-')
        assert False
    except TypeError as error:
        logger.debug(error)
    try:
        record.add_parameter('table', pd.DataFrame({'COL1': ["PARAM1", "PARAM2"], 'COL2': [
                             1, 2], 'COL3': [1.4, 1.5], 'COL4': [False, True]}))
        assert False
    except ValueError as error:
        logger.debug(error)


@pytest.mark.test_modules
def test_add_table():
    """Test EXF add_parameter method works."""
    from exf import EXF  # pylint: disable=import-outside-toplevel, unused-import
    try:
        record = EXF()
        record.add_table(None, pd.DataFrame({'COL1': ["PARAM1", "PARAM2"], 'COL2': [
                         1, 2], 'COL3': [1.4, 1.5], 'COL4': [False, True]}))
        assert False
    except ValueError as error:
        logger.debug(error)
    try:
        record = EXF()
        record.add_table(12, pd.DataFrame({'COL1': ["PARAM1", "PARAM2"], 'COL2': [
                         1, 2], 'COL3': [1.4, 1.5], 'COL4': [False, True]}))
        assert False
    except TypeError as error:
        logger.debug(error)


@pytest.mark.test_modules
def test_file_version():
    """Test File Version class works."""
    from exf import EXF  # pylint: disable=import-outside-toplevel, unused-import
    record = EXF("v1.0")
    record = EXF({'major': 1, 'minor': 0})
    assert record.file_version.major == 1
    assert record.file_version.to_dict()['major'] == 1
    assert record.file_version.to_string() == '1.0'
    try:
        record = EXF("1v.0")
        assert False
    except ValueError as error:
        logger.debug(error)
    try:
        record = EXF("1.0v")
        assert False
    except ValueError as error:
        logger.debug(error)
    try:
        record = EXF(file_version=['1', '0'])
        assert False
    except TypeError as error:
        logger.debug(error)


@pytest.mark.test_modules
def test_test_program():
    """Test Test Program class works."""
    from exf.main import TestProgram  # pylint: disable=import-outside-toplevel, unused-import
    try:
        record = TestProgram()
        assert False
    except TypeError as error:
        logger.debug(error)
    record = TestProgram('NAME', 'VERSION')
    record = TestProgram.parse({'name': 'NAME', 'revision': "REVISION"})
    try:
        record = TestProgram.parse(1.2)
        assert False
    except TypeError as error:
        logger.debug(error)
    try:
        record = TestProgram(None, 'VERSION')
        assert False
    except ValueError as error:
        logger.debug(error)
    try:
        record = TestProgram(123, 'REVISION')
        assert False
    except TypeError as error:
        logger.debug(error)

    try:
        record = TestProgram('NAME', None)

        assert False
    except ValueError as error:
        logger.debug(error)
    try:
        record = TestProgram('NAME', 1.0)
        assert False
    except TypeError as error:
        logger.debug(error)
    record.to_dict()
    record.to_string()
    print(record)


@pytest.mark.test_modules
def test_table():
    """Test Table class works."""
    from exf.main import Table  # pylint: disable=import-outside-toplevel, unused-import
    record = Table()
    try:
        record = Table({'key': 'value'})
        assert False
    except TypeError as error:
        logger.debug(error)
    try:
        record = Table([], {'key': 'value'})
        assert False
    except TypeError as error:
        logger.debug(error)
    try:
        record.add_column(1234)
        assert False
    except TypeError as error:
        logger.debug(error)
    record.add_column('COL1')
    try:
        record.add_column('COL1')
        assert False
    except ValueError as error:
        logger.debug(error)
    record.add_row([1.234])
    try:
        record.add_row([1.2, 1, 2])
        assert False
    except ValueError as error:
        logger.debug(error)

    try:
        record = Table.parse(None)
        assert False
    except ValueError as error:
        logger.debug(error)
    record = Table.parse(
        "COL1\tCOL2\tCOL3\tCOL4\nPARAM1\t1\t1.4\tFalse\nPARAM2\t2\t1.5\tTrue\n")
    record2 = Table.parse([{'COL1': 'PARAM1', 'COL2': 1, 'COL3': 1.4, 'COL4': False}, {
                          'COL1': 'PARAM2', 'COL2': 2, 'COL3': 1.5, 'COL4': True}])
    record3 = Table.parse({'COL1': ["PARAM1", "PARAM2"], 'COL2': [
                          1, 2], 'COL3': [1.4, 1.5], 'COL4': [False, True]})
    record4 = Table.parse(pd.DataFrame({'COL1': ["PARAM1", "PARAM2"], 'COL2': [
                          1, 2], 'COL3': [1.4, 1.5], 'COL4': [False, True]}))
    assert record.to_dict() == record2.to_dict(
    ) == record3.to_dict() == record4.to_dict()
    record5 = Table.parse({'COL1': ['PARAM1', 'PARAM2'], 'COL2': [
                          arrow.now('utc'), arrow.now('local')]})
    try:
        record = Table.parse([{'test1': ['a', 'b', 'c']}, 'test2', 'test3'])
    except ValueError as error:
        logger.debug(error)
    try:
        record = Table.parse(1.0)
    except TypeError as error:
        logger.debug(error)


@pytest.mark.test_modules
def test_exf():
    """Test main package works."""
    import exf  # pylint: disable=import-outside-toplevel, unused-import
    try:
        record = exf.read_exf(None)
        assert False
    except ValueError as error:
        logger.debug(error)
    try:
        record = exf.read_exf({})
        assert False
    except TypeError as error:
        logger.debug(error)
    record = exf.read_exf('tests/test1.exf')
    assert record.file_version.major == 1
    record.to_exf()
    record.to_exf('out/out.exf')
    record.to_exf('out/out2')
    record.to_json()
    record.to_json('out/out.json')
    with open('out/out.exf', 'r') as file_handle:
        data = file_handle.read()
        file_handle.close()
    record = exf.read_exf(StringIO(data))
    assert True


@pytest.mark.test_modules
def test_json():
    """Test main package works."""
    import exf  # pylint: disable=import-outside-toplevel, unused-import
    record = exf.read_json('tests/test1.json')
    assert record.file_version.major == 1
    assert True
