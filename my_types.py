import typing
from openpyxl.cell import Cell

AcceptedFileNames: typing.TypeAlias = typing.Literal[
    'restock_report',
    'inventory_file',
    'informed_csv'
]

Row: typing.TypeAlias = dict[str, typing.AnyStr]
Processor: typing.TypeAlias = typing.Optional[typing.Callable[[Row, Cell], typing.NoReturn]]
Validator: typing.TypeAlias = typing.Optional[typing.Callable[[typing.Any], bool]]
FileName: typing.TypeAlias = typing.Optional[AcceptedFileNames]
RowDataDict = typing.TypedDict('RowDataDict', {
    'inventory_row': Row,
    'informed_row': Row,
    'restock_row': Row
})
GREEN_COLOR = "00FF00"
RED_COLOR = "FF0000"
ORANGE_COLOR = "FFA500"


class MappedCell(typing.TypedDict):
    """A dictionary that maps a column name to a cell value from another file"""
    column_name: str  # The name of the column
    file_name: FileName  # The file it should be mapped from
    original_column_name: typing.Optional[str]  # the name of the column in the file that the column name is mapped from
    processor: Processor  # A function that processes the value of the cell
    validator: Validator # A function that validates the value of the cell


class MatchedRow(typing.TypedDict):
    inventory_row: typing.Dict[str, typing.AnyStr]
    informed_row: typing.Dict[str, typing.AnyStr]
    restock_row: typing.Dict[str, typing.AnyStr]
