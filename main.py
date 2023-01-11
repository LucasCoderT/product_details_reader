import collections
import contextlib
import typing

from openpyxl.cell import Cell
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet

from cell_mapping import OUTPUT_MAPPED_CELLS
from my_types import MatchedRow
from processors import find_restock_skus, find_all_rows_with_matching_skus
from utils import read_report


def generate_dict():
    """Generates a template dictionary from OUTPUT_MAPPED_CELLS column_name"""
    return {cell['column_name']: '' for cell in OUTPUT_MAPPED_CELLS}


def map_row(
        row_data: MatchedRow,
) -> dict:
    output_row_data = generate_dict()
    restock_row = row_data['restock_row']
    inventory_row = row_data['inventory_row']
    informed_row = row_data['informed_row']
    if not all([restock_row, inventory_row, informed_row]):
        raise ValueError("Not all rows were found")
    mapping = {
        'restock_report': restock_row,
        'inventory_file': inventory_row,
        'informed_csv': informed_row
    }

    for cell in OUTPUT_MAPPED_CELLS:
        file_name = cell.get('file_name')
        if file_name is None:
            continue
        original_column_name = cell['original_column_name']
        if original_column_name is None:
            original_column_name = cell['column_name']
        output_row_data[cell['column_name']] = mapping[file_name][original_column_name]

    # We have to wait for the row to be completely mapped so that we can process it
    return output_row_data


def process_row(mapped_row: dict, cell: Cell, column_name: str):
    for mapped_cell in [mapped_cell for mapped_cell in OUTPUT_MAPPED_CELLS if
                        mapped_cell['column_name'] == column_name]:
        if processor := mapped_cell.get('processor'):
            processor(mapped_row, cell)


def main():
    output_mapping: list = []
    invalid_rows = []
    # Read files
    restock_report = read_report('restock_report', read_only=True)
    inventory_file = read_report('inventory_file', read_only=True)
    informed_csv = read_report('informed_csv', read_only=True)

    skus = find_restock_skus(restock_report)
    # Find matching rows
    matched_row_data: typing.Dict[str, MatchedRow] = collections.defaultdict(
        lambda: {'inventory_row': {}, 'informed_row': {}, 'restock_row': {}})
    matched_restock_rows = find_all_rows_with_matching_skus(skus, restock_report)
    matched_inventory_rows = find_all_rows_with_matching_skus(skus, inventory_file, prefix="Parsing Inventory file")
    matched_informed_rows = find_all_rows_with_matching_skus(skus, informed_csv, prefix="Parsing Informed file")

    # Store data
    # Restock file
    for matched_restock_row_sku, matched_restock_row in matched_restock_rows.items():
        matched_row_data[matched_restock_row_sku]['restock_row'] = matched_restock_row
    # Inventory file
    for matched_inventory_row_sku, matched_inventory_row in matched_inventory_rows.items():
        matched_row_data[matched_inventory_row_sku]['inventory_row'] = matched_inventory_row
    # Informed file
    for matched_informed_row_sku, matched_informed_row in matched_informed_rows.items():
        matched_row_data[matched_informed_row_sku]['informed_row'] = matched_informed_row

    # Process rows
    for row_data in matched_row_data.values():
        try:
            mapped_row = map_row(row_data)
            output_mapping.append(mapped_row)
        except ValueError:
            invalid_rows.append(row_data)

    # Create Output Workbook
    headers = list(generate_dict().keys())
    wb = Workbook()
    ws: Worksheet = wb.active
    ws.append(headers)
    for row in output_mapping:
        ws.append(list(row.values()))
    # Loop over rows to process them via their processor in OUTPUT_MAPPED_CELLS
    for ws_row, output_row in zip(ws.iter_rows(min_row=2), output_mapping):
        for ws_cell, output_cell in zip(ws_row, output_row.keys()):
            process_row(output_row, ws_cell, headers[ws_cell.col_idx - 1])

    wb.save('output.xlsx')


if __name__ == '__main__':
    main()
