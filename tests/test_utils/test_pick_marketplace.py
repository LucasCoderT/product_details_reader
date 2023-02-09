import unittest.mock
from unittest import TestCase
from unittest.mock import MagicMock

import utils


@unittest.mock.patch('utils.exit')
@unittest.mock.patch('utils.print')
@unittest.mock.patch('utils.input')
class TestPickMarketPlace(TestCase):

    def test_pick_marketplace_correct_input(self, mock_input: MagicMock, mock_print: MagicMock, mock_exit: MagicMock):
        mock_input.return_value = '1'
        result = utils.pick_marketplace()
        self.assertEqual(result, 1)

    def test_pick_marketplace_invalid_number(self, mock_input: MagicMock, mock_print: MagicMock, mock_exit: MagicMock):
        mock_input.side_effect = ['a', '1']
        result = utils.pick_marketplace()
        self.assertEqual(result, 1)
        mock_print.assert_called_once_with("Please enter a valid marketplace ID")

    def test_pick_marketplace_with_empty_input(self, mock_input: MagicMock, mock_print: MagicMock,
                                               mock_exit: MagicMock):
        mock_input.side_effect = [None, '1']
        result = utils.pick_marketplace()
        self.assertEqual(result, 1)
        mock_print.assert_called_once_with("Please enter a marketplace ID")

    def test_pick_marketplace_quit(self, mock_input: MagicMock, mock_print: MagicMock, mock_exit: MagicMock):
        mock_input.return_value = 'quit'
        mock_exit.side_effect = SystemExit()
        self.assertRaises(SystemExit, utils.pick_marketplace)
        mock_exit.assert_called_once_with(0)
