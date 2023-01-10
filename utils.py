import csv
import difflib
import os
import typing

import openpyxl
from openpyxl.workbook import Workbook


def sanitize_cell_value(value: str) -> str:
    return clean_value(sanitize_names(value))


def lower_clean_cell_value(value: str) -> str:
    return sanitize_cell_value(value).lower()


def clean_value(value: str) -> str:
    """Remove all spaces and newlines from the value."""
    if value is None:
        return ''
    if isinstance(value, str):
        return value.replace(" ", "").replace("\n", "")
    return value


def sanitize_names(name: typing.Any) -> str:
    sanitized_name = str(name)

    if not sanitized_name:
        return ''
    if sanitized_name[0] == '\xa0':
        sanitized_name = sanitized_name.lstrip("\xa0")
    if sanitized_name[-1] == '\xa0':
        sanitized_name = sanitized_name.rstrip('\xa0')
    if "\xa0" in sanitized_name:
        sanitized_name = sanitized_name.replace("\xa0", " ")
    if sanitized_name[0] == " ":
        sanitized_name = sanitized_name.lstrip(" ")
    return sanitized_name


def transform_csv_to_xslx(csv_file):
    """Takes a csv file and creates an openpyxl Workbook object from it"""
    with open(csv_file, 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        wb = openpyxl.Workbook()
        ws = wb.active
        while True:
            try:
                try:
                    row = next(reader)
                except UnicodeDecodeError:
                    continue
                ws.append(row)
            except StopIteration:
                break
        return wb


def read_xslx_file(xlsx_file: str | Workbook, **kwargs):
    """Takes a xlsx file and returns a Workbook object"""
    if isinstance(xlsx_file, str):
        wb = openpyxl.load_workbook(xlsx_file, **kwargs)
    else:
        wb = xlsx_file
    ws = wb.active
    rows = list(ws.rows)
    header = [sanitize_names(cell.value) for cell in rows[0]]
    return [
        dict(zip(header, [clean_value(cell.value) for cell in row]))
        for row in rows[1:]
    ]


def find_file(file_name: str):
    """Finds the closest matching file in the current directory"""
    for root, dirs, files in os.walk("./files"):
        if closest_match := difflib.get_close_matches(file_name, files, n=1):
            closest_match: typing.List[str]
            return os.path.join(root, closest_match[0])
    return None


def read_report(file_name: str, **kwargs):
    file_path = find_file(file_name)

    if not file_path:
        raise FileNotFoundError(f"Could not find file {file_name}")

    if file_path.endswith(".xlsx"):
        return read_xslx_file(file_path, **kwargs)
    elif file_path.endswith((".csv", ".txt")):
        wb = transform_csv_to_xslx(file_path)
        return read_xslx_file(wb, **kwargs)
