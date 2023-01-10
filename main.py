import asyncio

import progressbar

from cell_mapping import OUTPUT_MAPPED_CELLS
from processors import find_row_by_sku, find_restock_skus, find_all_matching_skus
from utils import read_report


def generate_dict():
    """Generates a template dictionary from OUTPUT_MAPPED_CELLS column_name"""
    return {cell['column_name']: '' for cell in OUTPUT_MAPPED_CELLS}


async def process_row(row, output_mapping, inventory_file, informed_csv, progress_bar: progressbar.ProgressBar):
    output_row_data = generate_dict()
    try:
        sku_cell, inventory_row = find_row_by_sku(row['Merchant SKU'], inventory_file)
        for cell in OUTPUT_MAPPED_CELLS:
            output_row_data[cell['column_name']] = inventory_row[sku_cell]
    except ValueError:
        pass
    try:
        sku_cell, informed_row = find_row_by_sku(row['Merchant SKU'], informed_csv)
        for cell in OUTPUT_MAPPED_CELLS:
            output_row_data[cell['column_name']] = informed_row[sku_cell]
    except ValueError:
        pass
    output_mapping.append(output_row_data)
    progress_bar.increment(1)


async def main():
    output_mapping: list = []
    restock_report = read_report('restock_report', read_only=True)
    inventory_file = read_report('inventory_file', read_only=True)
    informed_csv = read_report('informed_csv', read_only=True)
    skus = find_restock_skus(restock_report)
    matching_skus = find_all_matching_skus(skus, inventory_file, prefix="Parsing Inventory file")
    print(matching_skus)

    # tasks = []
    # progress_bar = progressbar.ProgressBar(max_value=len(restock_report))
    # for row in restock_report:
    #     tasks.append(process_row(row, output_mapping, inventory_file, informed_csv, progress_bar))
    # progress_bar.start()
    # await asyncio.gather(*tasks)
    # with open('data.json', 'w+') as file:
    #     json.dump(output_mapping, file)


if __name__ == '__main__':
    asyncio.run(main())
