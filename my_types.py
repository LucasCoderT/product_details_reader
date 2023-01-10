import typing

from openpyxl.cell import Cell

AcceptedFileNames: typing.TypeAlias = typing.Literal[
    'restock_report',
    'inventory_file',
    'informed_csv'
]

Row: typing.TypeAlias = dict[str, typing.AnyStr]
Processor: typing.TypeAlias = typing.Optional[typing.Callable[[Row], typing.NoReturn]]
FileName: typing.TypeAlias = typing.Optional[AcceptedFileNames]

GREEN_COLOR = "00FF00"
RED_COLOR = "FF0000"
ORANGE_COLOR = "FFA500"


class MappedCell(typing.TypedDict):
    """A dictionary that maps a column name to a cell value from another file"""
    column_name: str  # The name of the column
    file_name: FileName  # The file it should be mapped from
    original_column_name: typing.Optional[str]  # the name of the column in the file that the column name is mapped from
    processor: Processor  # A function that processes the value of the cell
