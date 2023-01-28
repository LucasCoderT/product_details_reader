from common import read_files, find_skus, process_rows, create_output_workbook
from utils import pick_marketplace

if __name__ == '__main__':
    """
    Main function
    """
    market_place_id = pick_marketplace()
    files = read_files()
    matched_row_data = find_skus(*files, market_place_id=market_place_id)
    output_mapping = process_rows(matched_row_data)
    create_output_workbook(output_mapping)
