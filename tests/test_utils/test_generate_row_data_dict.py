import unittest

import utils


class TestGenerateRowDataDict(unittest.TestCase):

    def test_mapped_cell_dict_is_correct(self):
        expected_keys = [
            'inventory_row',
            'informed_row',
            'restock_row'
        ]
        mapped_cell_dict = utils.generate_row_data_dict()
        self.assertEqual(len(mapped_cell_dict), len(expected_keys))


if __name__ == '__main__':
    unittest.main()
