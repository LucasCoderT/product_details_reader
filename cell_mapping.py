import typing

from processors import \
    calculate_days_on_hand, \
    calculate_buy_box_color, \
    apply_number_style, \
    validate_number
from my_types import MappedCell
"""
This file contains a list of all the cells that are mapped from one file to another.
"""
OUTPUT_MAPPED_CELLS: typing.List[MappedCell] = [
    {
        'column_name': 'Merchant SKU',
        'file_name': 'restock_report',
        'original_column_name': 'Merchant SKU'
    },
    {
        'column_name': 'ASIN',
        'file_name': 'restock_report',
        'original_column_name': 'ASIN'
    },
    {
        'column_name': 'Product Name',
        'file_name': 'restock_report',
        'original_column_name': 'Product Name'
    },
    {
        'column_name': 'Part Number',
        'file_name': 'inventory_file',
        'original_column_name': 'Part Number'
    },
    {
        'column_name': 'Primary Supplier',
        'file_name': 'inventory_file',
        'original_column_name': 'Primary Supplier'
    },
    {
        'column_name': 'Classification',
        'file_name': 'inventory_file',
        'original_column_name': 'Classification'
    },
    {
        'column_name': 'Units Sold Last 30 Days',
        'file_name': 'restock_report',
        'original_column_name': 'Units Sold Last 30 Days',
        'processor': apply_number_style,
        'validator': validate_number
    },
    {
        'column_name': 'CURRENT_VELOCITY',
        'file_name': 'informed_csv',
        'original_column_name': 'CURRENT_VELOCITY'
    },
    {
        'column_name': 'Total Units',
        'file_name': 'restock_report',
        'original_column_name': 'Total Units',
        'processor': apply_number_style,
        'validator': validate_number
    },
    {
        'column_name': 'Days on Hand',
        'processor': calculate_days_on_hand,
        'validator': validate_number,
    },
    {
        'column_name': 'Quantity Available',
        'file_name': 'inventory_file',
        'original_column_name': 'Quantity Available',
        'processor': apply_number_style,
        'validator': validate_number
    },
    {
        'column_name': 'COST',
        'file_name': 'informed_csv',
        'original_column_name': 'COST',
        'processor': apply_number_style,
        'validator': validate_number,
    },
    {
        'column_name': 'MIN_PRICE',
        'file_name': 'informed_csv',
        'original_column_name': 'MIN_PRICE',
        'processor': apply_number_style,
        'validator': validate_number,
    },
    {
        'column_name': 'CURRENT_PRICE',
        'file_name': 'informed_csv',
        'original_column_name': 'CURRENT_PRICE',
        'processor': apply_number_style,
        'validator': validate_number,
    },
    {
        'column_name': 'BUY_BOX_PRICE',
        'file_name': 'informed_csv',
        'original_column_name': 'BUY_BOX_PRICE',
        'processor': calculate_buy_box_color,
        'validator': validate_number,
    },
    {
        'column_name': 'MAX_PRICE',
        'file_name': 'informed_csv',
        'original_column_name': 'MAX_PRICE',
        'processor': apply_number_style,
        'validator': validate_number,
    }
]
