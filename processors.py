import contextlib
import typing

from openpyxl.cell import Cell
from openpyxl.styles import PatternFill

from my_types import Row, GREEN_COLOR, RED_COLOR, ORANGE_COLOR, MatchedRow
from utils import lower_clean_cell_value, generate_mapped_cell_dict


def find_all_rows_with_matching_skus(skus: typing.List[str], rows: typing.Iterable[Row], *, prefix: str = None,
                                     market_place_id: typing.Optional[str] = None) -> \
        typing.Dict[str, Row]:
    """Finds all rows that have a matching sku from a given list of skus"""
    unfounded_skus = {
        lower_clean_cell_value(sku): True for sku in skus
    }
    rows = list(rows)
    cols = []
    found_rows = {}
    for row in rows:
        if market_place_id:
            row_market_place_id = get_cell(row, 'MARKETPLACE_ID')
            if row_market_place_id and row_market_place_id != market_place_id:
                continue
        if not cols:
            cols = [key for key in row.keys() if 'sku' in key.lower()]
        for sku_cell in cols:
            lower = lower_clean_cell_value(row[sku_cell])
            if lower in unfounded_skus:
                unfounded_skus.pop(lower)
                found_rows[lower] = row
                break

    return found_rows


def find_restock_skus(rows: typing.Iterable[Row]) -> typing.List[str]:
    return [row['Merchant SKU'] for row in rows]


def find_all_columns_headers(headers: typing.List[str], column_name: str) -> typing.List[str]:
    """Finds all column headers that contain name"""
    return [key for key in headers if column_name.lower() in key.lower()]


def get_cell(row: Row, column_name: str) -> str:
    """
    Takes a Row and finds the column with the
    value column_name and returns the value of the cell in that column.
    """
    for cell in row:
        if lower_clean_cell_value(cell) == lower_clean_cell_value(column_name):
            return row[cell]


def calculate_days_on_hand(row: Row, cell: Cell) -> typing.NoReturn:
    total_units = get_cell(row, 'Total Units')
    units_sold = get_cell(row, 'Units Sold Last 30 Days')
    if not total_units or not units_sold:
        cell.value = ''
        return
    total_units = float(total_units)
    units_sold = float(units_sold)
    try:
        result = (total_units / units_sold) * 30
        cell.number_format = '0.00'
    except ZeroDivisionError:
        result = "Infinity"
    cell.value = result


def calculate_buy_box_color(row: Row, cell: Cell) -> typing.NoReturn:
    """Applies a style to the cell based on the value of the cell"""
    buy_box_price_cell = get_cell(row, 'BUY_BOX_PRICE')
    min_price = get_cell(row, 'MIN_PRICE')
    max_price = get_cell(row, 'MAX_PRICE')
    if not min_price or not max_price or not buy_box_price_cell:
        return
    buy_box_price = float(buy_box_price_cell)
    min_price = float(min_price)
    max_price = float(max_price)
    # if min_price < buy_box_price < max_price colour green:
    if min_price < buy_box_price < max_price:
        color = GREEN_COLOR
    elif min_price >= buy_box_price:
        color = RED_COLOR
    else:
        color = ORANGE_COLOR
    cell.fill = PatternFill(start_color=color, end_color=color, fill_type='solid')
    cell.number_format = '0.00'


def apply_number_style(row: Row, cell: Cell) -> typing.NoReturn:
    """Applies a number style to the cell"""
    cell.number_format = '0.00'
    if cell.value:
        cell.value = float(cell.value)


def process_row(mapped_row: dict, cell: Cell, column_name: str):
    from cell_mapping import OUTPUT_MAPPED_CELLS
    for mapped_cell in [mapped_cell for mapped_cell in OUTPUT_MAPPED_CELLS if
                        mapped_cell['column_name'] == column_name]:
        if processor := mapped_cell.get('processor'):
            processor(mapped_row, cell)


def map_row(
        row_data: MatchedRow,
) -> dict:
    from cell_mapping import OUTPUT_MAPPED_CELLS
    output_row_data = generate_mapped_cell_dict()
    restock_row = row_data['restock_row']
    inventory_row = row_data['inventory_row']
    informed_row = row_data['informed_row']
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
        with contextlib.suppress(KeyError):
            output_row_data[cell['column_name']] = mapping[file_name][original_column_name]
    # We have to wait for the row to be completely mapped so that we can process it
    return output_row_data
