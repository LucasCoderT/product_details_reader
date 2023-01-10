import typing

import progressbar
from openpyxl.styles import Color

from my_types import Row, GREEN_COLOR, RED_COLOR, ORANGE_COLOR
from utils import lower_clean_cell_value


def find_all_matching_skus(skus: typing.List[str], rows: typing.Iterable[Row], *, prefix: str = None) -> typing.List[typing.Tuple[str, Row]]:
    """Finds all the skus from the file"""
    unfounded_skus = list(skus)
    num_rows = len(unfounded_skus)
    found_rows = []
    for row in progressbar.progressbar(rows, max_value=num_rows, prefix=prefix):
        found_sku = False
        for sku_cells in get_cells_by_column_name(row, 'sku'):
            for sku_cell in sku_cells:
                for sku in unfounded_skus:
                    if lower_clean_cell_value(row[sku_cell]) == lower_clean_cell_value(sku):
                        unfounded_skus.remove(sku)
                        found_rows.append((sku_cell, row))
                        found_sku = True
                        break
                if found_sku:
                    break
            if found_sku:
                break

    return found_rows


def find_restock_skus(rows: typing.Iterable[Row]) -> typing.List[str]:
    skus = []
    for row in rows:
        skus.append(row['Merchant SKU'])
    return skus


def find_row_by_sku(sku: str, inventory_file: typing.Iterable[Row]) -> typing.Optional[
    typing.Tuple[str, Row]]:
    """Finds the row in the inventory file that matches the sku in the row"""
    for row, sku_cells in get_cells_by_column_name(inventory_file, 'SKU'):
        for sku_cell in sku_cells:
            if lower_clean_cell_value(row[sku_cell]) == lower_clean_cell_value(sku):
                return sku_cell, row
    raise ValueError(f"Could not find sku {sku} in inventory file")


def get_cells_by_column_name(row: Row, column_name: str) -> typing.Iterable[str]:
    """Gets all cells in a row that have the value column_name in the column"""
    if closest_matches := [key for key in row.keys() if column_name.lower() in key.lower()]:
        closest_matches: typing.List[str]
        yield closest_matches


def get_cell(row: Row, column_name: str) -> str:
    """
    Gets an openpyxl Row and finds the column with the
    value column_name and returns the value of the cell in that column.
    """
    for cell in row:
        if lower_clean_cell_value(cell) == lower_clean_cell_value(column_name):
            return row[cell]


def calculate_days_on_hand(row: Row) -> str:
    total_units = float(get_cell(row, 'Total Units'))
    units_sold = float(get_cell(row, 'Units Sold Last 30 Days'))
    try:
        result = str((total_units / units_sold) * 30)
    except ZeroDivisionError:
        result = "Infinity"
    return result


def calculate_buy_box_color(row: Row) -> Color:
    """Applies a style to the cell based on the value of the cell"""
    buy_box_price_cell = get_cell(row, 'BUY_BOX_PRICE')
    buy_box_price = float(buy_box_price_cell)
    min_price = float(get_cell(row, 'MIN_PRICE'))
    max_price = float(get_cell(row, 'MAX_PRICE'))
    # if min_price < buy_box_price < max_price colour green:
    if min_price < buy_box_price < max_price:
        return GREEN_COLOR
    elif min_price >= buy_box_price:
        return RED_COLOR
    else:
        return ORANGE_COLOR
