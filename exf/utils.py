"""Shared utils."""
import os
from io import StringIO
import json
from datetime import date, datetime
from typing import Dict, Union, Any, List, Optional
from loguru import logger
from arrow.arrow import Arrow
import pandas as pd
from .config import ENCODING, ENVIRONMENT


def validate_path(dir_path: str, permission: str = 'r') -> bool:
    """Validate folder permissions."""
    if not os.path.exists(dir_path):
        try:
            full_path = os.path.abspath(dir_path)
            base_path = os.path.split(full_path)[0]
            if base_path != full_path:
                validate_path(base_path)
            os.mkdir(dir_path)
        except Exception as error:
            logger.error(f"Failed to create path: {dir_path}")
            logger.debug(error)
            raise ValueError(f"Path not found: {dir_path}") from error
    if not os.path.isdir(dir_path):
        raise TypeError(f"Path not directory: {dir_path}")
    if permission.lower() == 'r':
        if not os.access(dir_path, os.R_OK):
            raise ValueError(f"Path not readable: {dir_path}")
    if permission.lower() == 'w':
        if not os.access(dir_path, os.W_OK):
            raise PermissionError(f"Path not writable: {dir_path}")
    return True


def validate_file(file_path: str, permission: str = 'r', validate_extension: bool = True) -> bool:
    """Validate file permissions."""
    if not os.path.exists(file_path):
        raise ValueError(f"File not found: {file_path}")
    if not os.path.isfile(file_path):
        raise TypeError(f"Provided path is not file: {file_path}")
    if permission.lower() == 'r':
        if not os.access(file_path, os.R_OK):
            raise PermissionError(f"File not readable: {file_path}")
    elif permission.lower() == 'w':
        if not os.access(file_path, os.W_OK):
            raise PermissionError(f"File not writable: {file_path}")
    else:
        raise ValueError(f"Invalid permission flag: {permission}")
    if validate_extension:
        file_ext = os.path.splitext(file_path)[1]
        if file_ext.startswith('.'):
            file_ext = file_ext[1:]
        if file_ext == '':
            raise ValueError(f"File has no extension: {file_path}")
    return True


def read_json(file_path: Union[str, StringIO]) -> Dict[str, Any]:
    """Read JSON record into class."""
    if isinstance(file_path, str):
        validate_file(file_path, permission='r')
        logger.debug(f"Reading File: {file_path}")
        with open(file_path, 'r', encoding=ENCODING) as file_handle:
            data = json.load(file_handle)
            file_handle.close()
    elif isinstance(file_path, StringIO):
        data = json.load(file_path)
    else:
        raise TypeError("Must provide json file or dictionary object.")
    return data


def read_dir(dir_path: str) -> List[str]:
    """Validate directory exists and return it's contents."""
    validate_path(dir_path, permission='r')
    return os.listdir(dir_path)


def sanitize_json(record):
    """Sanitize JSON object."""
    if record is None:
        return record
    if isinstance(record, (date, datetime, Arrow)):
        return str(record)
    if 'float' in str(type(record)).lower():
        return round(float(record), 15)
    if isinstance(record, list):
        return [sanitize_json(x) for x in record]
    if isinstance(record, dict):
        return {key: sanitize_json(value) for key, value in record.items()}
    if isinstance(record, pd.DataFrame):
        return sanitize_json(record.to_dict('records'))
    if pd.isnull(record):
        return None
    return record


def write_json(data: Dict[str, Any], file_path: Optional[str], permission=0o664) -> Optional[str]:
    """Write data to JSON file."""
    logger.info("WRITE_JSON: STARTED")
    if data is None:
        raise ValueError("No data to save.")
    if file_path is None:
        # output string
        return json.dumps(data, indent=4, sort_keys=False, default=sanitize_json)

    save_path, file_name = os.path.split(file_path)
    logger.debug(f"SAVE_PATH: {save_path}")
    logger.debug(f"file_name: {file_name}")
    validate_path(save_path, permission='w')
    file_name, file_ext = os.path.splitext(file_name)
    temp_path = os.path.join(save_path, file_name)
    if file_ext == '':
        file_ext = '.json'

    with open(temp_path, 'w', encoding=ENCODING) as file_handle:
        if ENVIRONMENT == "PRODUCTION":
            json.dump(data, file_handle,
                      sort_keys=False, default=sanitize_json)
        else:
            json.dump(data, file_handle, indent=4,
                      sort_keys=False, default=sanitize_json)
        file_handle.close()
    final_path = temp_path + file_ext
    os.replace(temp_path, final_path)
    os.chmod(final_path, permission)
    logger.info(f"FILE SAVED: {final_path}")
    return None
