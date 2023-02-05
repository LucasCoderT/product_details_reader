import traceback

from common import read_files, find_skus, process_rows, create_output_workbook
from utils import pick_marketplace

if __name__ == '__main__':
    """
    Main function
    """
    try:
        market_place_id = pick_marketplace()
        files = read_files()
        matched_row_data = find_skus(*files, market_place_id=market_place_id)
        output_mapping = process_rows(matched_row_data)
        create_output_workbook(output_mapping)
    except Exception as error:
        traceback.print_tb(error.__traceback__)
        input("Press enter to exit...")
