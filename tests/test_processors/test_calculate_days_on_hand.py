import unittest.mock

import processors
from my_types import Row


@unittest.mock.patch('processors.Cell')
class TestCalculateDaysOnHand(unittest.TestCase):

    def test_calculate_days_on_hand_valid_inputs(self, mock_cell: unittest.mock.MagicMock):
        total_units = 100
        units_sold_last_30_days = 10
        data: Row = {
            'Total Units': str(total_units),
            'Units Sold Last 30 Days': str(units_sold_last_30_days),
        }
        expected_result = (total_units / units_sold_last_30_days) * 30
        mock_cell.value = None
        self.assertEqual(mock_cell.value, None)
        processors.calculate_days_on_hand(data, mock_cell)
        self.assertEqual(mock_cell.value, expected_result)

    def test_calculate_days_on_hand_both_zero_inputs(self, mock_cell: unittest.mock.MagicMock):
        data: Row = {
            'Total Units': '0',
            'Units Sold Last 30 Days': '0',
        }
        expected_result = 1
        mock_cell.value = None
        self.assertEqual(mock_cell.value, None)
        processors.calculate_days_on_hand(data, mock_cell)
        self.assertEqual(mock_cell.value, expected_result)

    def test_calculate_days_on_hand_division_by_zero_returns_infinity(self, mock_cell: unittest.mock.MagicMock):
        data: Row = {
            'Total Units': '1',
            'Units Sold Last 30 Days': '0',
        }
        expected_result = 'Infinity'
        mock_cell.value = None
        self.assertEqual(mock_cell.value, None)
        processors.calculate_days_on_hand(data, mock_cell)
        self.assertEqual(mock_cell.value, expected_result)

    def test_calculate_days_on_hand_missing_total_units(self, mock_cell: unittest.mock.MagicMock):
        data: Row = {
            'Units Sold Last 30 Days': '1',
        }
        expected_result = ''
        mock_cell.value = None
        self.assertEqual(mock_cell.value, None)
        processors.calculate_days_on_hand(data, mock_cell)
        self.assertEqual(mock_cell.value, expected_result)

    def test_calculate_days_on_hand_missing_units_sold_last_30_days(self, mock_cell: unittest.mock.MagicMock):
        data: Row = {
            'Total Units': '1',
        }
        expected_result = ''
        mock_cell.value = None
        self.assertEqual(mock_cell.value, None)
        processors.calculate_days_on_hand(data, mock_cell)
        self.assertEqual(mock_cell.value, expected_result)

    def test_calculate_days_on_hand_missing_both_total_units_and_units_sold_last_30_days(self,
                                                                                         mock_cell: unittest.mock.MagicMock):
        data: Row = {}
        expected_result = ''
        mock_cell.value = None
        self.assertEqual(mock_cell.value, None)
        processors.calculate_days_on_hand(data, mock_cell)
        self.assertEqual(mock_cell.value, expected_result)


if __name__ == '__main__':
    unittest.main()
