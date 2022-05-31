"""Main program."""
from io import StringIO
from typing import Dict, Any, List, Optional, Union
from datetime import datetime
from dateutil import parser
import arrow
import pandas as pd
from loguru import logger
from .config import ENCODING
from . import utils
__ALL__ = ['EXF', 'read_exf', 'read_json']


class FileVersion():
    """File Version class."""
    __major: int
    __minor: int

    def __init__(self, major=1, minor=0):
        """Initialize class."""
        self.major = major
        self.minor = minor

    @property
    def major(self) -> int:
        """Return Major version."""
        return self.__major

    @major.setter
    def major(self, value) -> None:
        """Set Major Version."""
        if not isinstance(value, int):
            try:
                value = int(str(value).strip())
            except (ValueError, TypeError) as error:
                logger.debug(error)
                raise ValueError(
                    f"Failed to parse Major Version: {value}") from error
        self.__major = value

    @property
    def minor(self) -> int:
        """Return Minor Version."""
        return self.__minor

    @minor.setter
    def minor(self, value) -> None:
        """Set Minor Version."""
        if not isinstance(value, int):
            try:
                value = int(str(value).strip())
            except (ValueError, TypeError) as error:
                logger.debug(error)
                raise ValueError(
                    f"Failed to parse Minor Version: {value}") from error
        self.__minor = value

    @classmethod
    def parse(cls, file_version: Union[str, Dict[str, int]]):
        """Parse string into class."""
        logger.info('Parse File Version')
        logger.debug(f"INPUT: {file_version}")

        major: Optional[Union[str, int]] = None
        minor: Optional[Union[str, int]] = None
        if isinstance(file_version, dict):
            major = file_version.get('major')
            minor = file_version.get('minor')
            return cls(major, minor)
        if not isinstance(file_version, str):
            raise TypeError("Input must be string.")
        if file_version[0].lower() == 'v':
            file_version = file_version[1:]
        major, minor = file_version.strip().split('.', 1)
        return cls(major, minor)

    def to_string(self):
        """Output string."""
        return f"{self.major}.{self.minor}"

    def to_dict(self):
        """Output dictionary."""
        return {'major': self.major, 'minor': self.minor}

    def __repr__(self):
        return self.to_string()


class TestProgram():
    """EXF Test Program class."""
    __name: str
    __revision: str

    def __init__(self, test_program: str, test_revision: str):
        """Initialize Class."""
        self.name = test_program
        self.revision = test_revision

    @ property
    def name(self) -> str:
        """Name Getter."""
        return self.__name

    @ name.setter
    def name(self, value: str) -> None:
        """Name Setter."""
        if value is None:
            raise ValueError("TestProgram Name cannot be None.")
        if not isinstance(value, str):
            raise TypeError(f"TestProgram->Name must be string: {value}")
        self.__name = value.strip()

    @ property
    def revision(self) -> str:
        """Revision Getter."""
        return self.__revision

    @ revision.setter
    def revision(self, value: str) -> None:
        """Revision Setter."""
        if value is None:
            raise ValueError("TestProgram Revision cannot be None.")
        if not isinstance(value, str):
            raise TypeError(f"TestProgram->Revision must be string: {value}")
        self.__revision = value.strip()

    @ classmethod
    def parse(cls, value: Union[str, Dict[str, str]]):
        """Parse string."""
        logger.info("Parse Test Program")
        logger.debug(f"INPUT: {value}")

        name: str = ""
        revision: str = ""
        if isinstance(value, dict):
            name = value.get('name', "")
            revision = value.get('revision', "")
            return cls(name, revision)
        if not isinstance(value, str):
            raise TypeError("Input must be string.")
        name, revision = value.split(' ', 1)
        return cls(name, revision)

    def to_string(self) -> str:
        """Return string representation of TestProgram."""
        return f"{self.name} {self.revision}"

    def to_dict(self) -> Dict[str, str]:
        """Return Dictionary representation of TestProgram."""
        return {'name': self.name, 'revision': self.revision}

    def __repr__(self):
        return self.to_string()


class Table():
    """Table class."""
    __table: pd.DataFrame
    __columns: Dict[str, str]

    def __init__(self, column_names: List[str] = [], column_types: List[Any] = []):
        """Initialize Class."""
        self.__columns = {}
        self.__table = pd.DataFrame(columns=column_names)
        if not isinstance(column_names, list):
            raise TypeError("column_names must be list of strings.")
        if not isinstance(column_types, list):
            raise TypeError("column_types must be list.")
        while len(column_names) > 0:
            column = column_names.pop(0)
            column_type = column_types.pop(0) if len(
                column_types) > 0 else float
            self.add_column(column, column_type)

    def add_column(self, column_name: str, column_type=float) -> None:
        """Add Column."""
        if not isinstance(column_name, str):
            raise TypeError("Input must be string.")
        if column_name in self.__columns:
            raise ValueError(f"Column Name already exists: {column_name}")
        self.__columns[column_name] = column_type
        self.__table[column_name] = pd.NA
        self.__table[column_name] = self.__table[column_name].astype(
            column_type)

    def add_row(self, data: List[Any]) -> None:
        """Add row data."""
        self.__table.loc[len(self.__table.index)] = data

    @classmethod
    def parse(cls, data: Union[str, pd.DataFrame]):
        """Parse String."""
        if data is None:
            raise ValueError("Table data cannot be None.")
        if isinstance(data, str):
            table: pd.DataFrame = pd.read_csv(StringIO(data), sep='\t')
        elif isinstance(data, pd.DataFrame):
            table = data.reset_index(drop=True)
        elif isinstance(data, (dict, list)):
            try:
                table = pd.DataFrame(data)
                logger.debug(table)
            except Exception as error:
                logger.debug(error)
                raise ValueError("Failed to parse Table data.") from error
        else:
            raise TypeError(f"Invalid data type for table: {type(data)}")
        column_names: List[str] = []
        column_types: List[type] = []
        for column in table.columns:
            column_names.append(column)
            if table[column].dtypes.name == 'bool':
                column_types.append(bool)
            elif table[column].dtypes.name.startswith('int'):
                column_types.append(int)
            elif table[column].dtypes.name.startswith('float'):
                column_types.append(float)
            else:
                column_types.append(table[column].dtypes.type)
        record = cls(column_names, column_types)
        for row in table.values:
            record.add_row(row)
        return record

    def to_dict(self) -> List[Dict[str, Any]]:
        """Return dictionary of table."""
        return self.__table.to_dict('records')

    def to_string(self) -> str:
        """Return String Representation."""
        return self.__table.to_csv(sep='\t', index=False)


class EXF():
    """Example file class."""
    file_version: FileVersion
    file_date: arrow.Arrow

    def __init__(self, file_version="1.0", **kwargs):
        """Initialize class."""
        if not isinstance(file_version, FileVersion):
            file_version = FileVersion.parse(file_version)
        self.file_version = file_version
        self.file_date = arrow.now()
        for key, value in kwargs.items():
            key = key.lower()
            logger.debug(f"{key}: {value}")
            if isinstance(value, (dict, list, pd.DataFrame)) and key not in ['test_program']:
                self.add_table(key, value)
            else:
                self.add_parameter(key, value)

    def add_parameter(self, key: str, value: Any):
        """Add parameter to file."""
        if key is None:
            raise ValueError("Parameter Key cannot be None.")
        if not isinstance(key, str):
            raise TypeError("Parameter Key must be string.")
        if isinstance(value, pd.DataFrame):
            raise ValueError(
                "Tables must be added using the add_table method.")
        if key == 'test_program' and not isinstance(value, TestProgram):
            value = TestProgram.parse(value)
        elif key.endswith('_date') and not isinstance(value, arrow.Arrow):
            if isinstance(value, str):
                try:
                    value = parser.parse(value)
                except parser.ParserError as error:
                    logger.debug(error)
                    raise ValueError(
                        f"Failed to parse date: {key} -> {value}") from error
            if isinstance(value, datetime) and value.tzinfo is None:
                value = arrow.get(value, tzinfo='local')
            else:
                try:
                    value = arrow.get(value)
                except Exception as error:
                    logger.debug(error)
                    raise ValueError(
                        f"Failed to parse date: {key} -> {value}") from error

        setattr(self, key, value)

    def add_table(self, key: str, data: pd.DataFrame = pd.DataFrame) -> None:
        """Add Table to dataset."""
        if key is None:
            raise ValueError("Table Key cannot be None.")
        if not isinstance(key, str):
            raise TypeError("Table Key must be string.")
        setattr(self, key, Table.parse(data))

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Parse Dictionary."""
        if data is None:
            raise ValueError("Data cannot be None.")
        if not isinstance(data, dict):
            raise TypeError("Data must be Dictionary.")
        data = dict(zip(list(map(str.lower, data.keys())), data.values()))
        if 'file_version' not in data:
            raise ValueError("File Version not found.")
        file_version = data.pop('file_version')

        return cls(file_version, **data)

    @classmethod
    def from_string(cls, data: str):
        """Parse String."""
        if data is None:
            raise ValueError("Data cannot be None.")
        if not isinstance(data, str):
            raise TypeError("Data must be string.")
        lines = data.strip().split('\n')
        line = lines.pop(0).strip()
        if not line.startswith("Example File "):
            raise ValueError("File Version not found.")
        args = {'file_version': line.split(' ')[-1]}
        while len(lines) > 0:
            line = lines.pop(0).strip()
            if line.startswith('#'):
                continue
            temp: List[str] = line.split(':', 1)

            key: str = temp[0].strip()
            value: str = temp[1].strip() if len(temp) > 1 else ''
            if value == '':
                found_end = False
                while len(lines) > 0:
                    line = lines.pop(0)
                    if line.upper().strip() == 'END':
                        found_end = True
                        break
                    value += line + "\n"
                if not found_end:
                    raise ValueError(
                        f"Failed to find END statement for key: {key}")
                args[key] = Table.parse(value)
                continue
            args[key] = value
        return cls(**args)

    def to_dict(self) -> Dict[str, Any]:
        """Return Dictionary representation of Example file."""
        out = {}
        for key, value in self.__dict__.items():
            # if key.startswith('_'):
            #     continue
            if hasattr(value, 'to_dict'):
                out[key] = value.to_dict()
                continue
            out[key] = value
        return out

    def to_string(self) -> str:
        """Return String of EXF data."""
        out = f"Example File v{self.file_version}\n"
        for key, value in self.__dict__.items():
            if key == 'file_version':
                continue
            if isinstance(value, Table):
                value = f"\n{value.to_string()}END"
            elif hasattr(value, 'to_string'):
                value = value.to_string()
            out += f"{key.upper()}: {value}\n"
        return out

    def to_exf(self, file_path: Optional[str] = None) -> Optional[str]:
        """Save EXF to file."""
        return utils.write_exf(self.to_string(), file_path)

    def to_json(self, file_path: Optional[str] = None) -> Optional[str]:
        """Save EXF to json file."""
        return utils.write_json(self.to_dict(), file_path)


def read_exf(file_path: Union[str, StringIO]) -> EXF:
    """Read exf file into class."""
    logger.info("Read EXF file.")
    logger.debug(f"FILE_PATH: {file_path}")
    if file_path is None:
        raise ValueError("File Path cannot be None.")
    if isinstance(file_path, str):
        with open(file_path, 'r', encoding=ENCODING) as file_handle:
            data = file_handle.read()
            file_handle.close()
    elif isinstance(file_path, StringIO):
        data = file_path.getvalue()
    else:
        raise TypeError(f"Invalid file_path type: {type(file_path)}")
    return EXF.from_string(data)


def read_json(file_path: Union[str, StringIO]) -> EXF:
    """Read json file into class."""
    logger.info("Read JSON file.")
    logger.debug(f"FILE_PATH: {file_path}")
    data = utils.read_json(file_path)
    return EXF.from_dict(data)
