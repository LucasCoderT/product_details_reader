import collections
import typing
from datetime import datetime

import progressbar
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet

from my_types import MatchedRow
from processors import find_restock_skus, find_all_rows_with_matching_skus, map_row, process_row
from utils import read_report, generate_row_data_dict, generate_mapped_cell_dict


def read_files():
    # Read files
    restock_report = read_report('restock_report', read_only=True)
    inventory_file = read_report('inventory_file', read_only=True)
    informed_csv = read_report('informed_csv', read_only=True)
    return restock_report, inventory_file, informed_csv


def find_skus(restock_report: typing.List[dict], inventory_file, informed_csv, *,
              market_place_id: typing.Optional[str] = None):
    # Find SKUs
    try:
        skus = find_restock_skus(restock_report)
    except KeyError:
        print("No SKUs found in restock report")
        return
    # Find matching rows
    matched_row_data: typing.Dict[str, MatchedRow] = collections.defaultdict(generate_row_data_dict)
    matched_restock_rows = find_all_rows_with_matching_skus(skus, restock_report)
    matched_inventory_rows = find_all_rows_with_matching_skus(skus, inventory_file, prefix="Parsing Inventory file")
    matched_informed_rows = find_all_rows_with_matching_skus(skus, informed_csv, prefix="Parsing Informed file",
                                                             market_place_id=market_place_id, )

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

    return matched_row_data


def process_rows(matched_row_data) -> typing.List[dict]:
    # Process rows
    print('Processing rows', end='')
    output_mapping: list = []
    for row_data in matched_row_data.values():
        mapped_row = map_row(row_data)
        output_mapping.append(mapped_row)
    print('...Done')
    return output_mapping


def create_output_workbook(output_mapping):
    # Create Output Workbook

    print('Creating output workbook')
    # Creates the headers
    headers = list(generate_mapped_cell_dict().keys())
    # Creates the workbook and worksheet
    wb = Workbook()
    ws: Worksheet = wb.active
    # Appends the headers to the worksheet
    ws.append(headers)
    # Appends the rows to the worksheet
    for row in output_mapping:
        ws.append(list(row.values()))
    # Zips the rows with the output mapping
    zipped_rows = zip(ws.iter_rows(min_row=2), output_mapping)
    bar = progressbar.progressbar(zipped_rows, max_value=len(output_mapping))
    # Loop over rows to process them via their processor in OUTPUT_MAPPED_CELLS
    for ws_row, output_row in bar:
        for ws_cell, output_cell in zip(ws_row, output_row.keys()):
            process_row(output_row, ws_cell, headers[ws_cell.col_idx - 1])
    # Save the workbook
    now = datetime.now()
    output_file_name = f'output_{now.strftime("%Y-%m-%d_%H-%M")}.xlsx'
    wb.save(output_file_name)
    print(f'Saved output file as {output_file_name}')
