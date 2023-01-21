from common import read_files, find_skus, process_rows, create_output_workbook

if __name__ == '__main__':
    files = read_files()
    matched_row_data = find_skus(*files)
    output_mapping = process_rows(matched_row_data)
    create_output_workbook(output_mapping)
