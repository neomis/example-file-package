# Example File

Python package to create and manipulate Example files.

## Installation

```bash
python -m venv exf
source exf/bin/activate
pip install --upgrade pip setuptools wheel
pip install exf
```

## Usage

`exf_to_json <file1.exf> [<out_path> --loglevel=(DEBUG|INFO|ERROR)]`
`json_to_exf <file1.json> [<out_path> --loglevel=(DEBUG|INFO|ERROR)]`

## Sample file

```text
Example File v1.0
# This is an example file used for parsing.
START_DATE: 2022-05-22 05:18:00
LOT_ID: LOT0001
WAFER_ID: WAFERSCRIBE01
TECHNOLOGY_ID: TECH01
DEVICE_ID: DEVICE01
OPERATION_ID: T2300.01
EQUIPMENT_ID: PROBER01
TEST_PROGRAM: MEASURE_THE_WAFER 1.0
INPUT_CONFIG:
TEMP	VDD	FSTART	FEND
80	2.4	1000	10000
END
# Table Data
DATA:
INDEX	PARAM	VALUE	PASS
1	PARAM1	1.0	TRUE
2	PARAM1	1.5	TRUE
3	PARAM2	1.6	TRUE
4	PARAM2	5	FALSE
END
END_DATE: 2022-05-22 05:20:00
```
