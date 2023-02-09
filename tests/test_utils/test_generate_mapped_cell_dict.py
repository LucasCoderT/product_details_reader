import unittest

import utils
from cell_mapping import OUTPUT_MAPPED_CELLS


class TestGenerateMappedCellDict(unittest.TestCase):

    def test_mapped_cell_dict_is_correct(self):
        mapped_cell_dict = utils.generate_mapped_cell_dict()
        self.assertEqual(len(mapped_cell_dict), len(OUTPUT_MAPPED_CELLS))
        for cell in OUTPUT_MAPPED_CELLS:
            self.assertIn(cell['column_name'], mapped_cell_dict)


if __name__ == '__main__':
    unittest.main()
