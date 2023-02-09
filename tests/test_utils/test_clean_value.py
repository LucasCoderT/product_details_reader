import unittest

import utils


class TestCleanValue(unittest.TestCase):

    def test_sanitize_cell_value_spaces_around(self):
        value = " TT "
        self.assertEqual(utils.sanitize_cell_value(value), "TT")

    def test_sanitize_cell_value_special_characters_end(self):
        value = "TT\xa0"
        self.assertEqual(utils.sanitize_cell_value(value), "TT")

    def test_sanitize_cell_value_special_characters_start(self):
        value = "\xa0TT"
        self.assertEqual(utils.sanitize_cell_value(value), "TT")

    def test_sanitize_cell_value_special_characters_middle(self):
        value = "T\xa0T"
        self.assertEqual(utils.sanitize_cell_value(value), "T T")

    def test_sanitize_cell_value_newlines_removed(self):
        value = "T\n"
        self.assertEqual(utils.sanitize_cell_value(value), "T")

    def test_sanitize_cell_value_none(self):
        value = None
        self.assertEqual(utils.sanitize_cell_value(value), "")


if __name__ == '__main__':
    unittest.main()
