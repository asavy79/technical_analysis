import unittest
import pandas as pd
import numpy as np
from src.indicators import MovingAverage
from src.main import Stock
import yfinance as yf
from unittest.mock import patch, MagicMock


class TestSimpleMovingAverage(unittest.TestCase):
    def setUp(self):
        # Create sample data for testing
        self.sample_data = pd.DataFrame({
            'Close': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        }, index=pd.date_range(start='2024-01-01', periods=10))

        # Mock the Stock class
        self.mock_stock = MagicMock(spec=Stock)
        self.mock_stock.get_period.return_value = 10
        self.mock_stock.get_ticker.return_value = "AAPL"

        # Mock yfinance response
        self.mock_history = MagicMock()
        self.mock_history.__getitem__.return_value = self.sample_data['Close']

    @patch('yfinance.Ticker')
    def test_sma_calculation(self, mock_ticker):
        # Setup mock
        mock_ticker_instance = MagicMock()
        mock_ticker_instance.history.return_value = self.sample_data
        mock_ticker.return_value = mock_ticker_instance

        # Test SMA with period 3
        sma = MovingAverage(period=3)
        result = sma.compute(self.mock_stock)

        # Expected values for 3-period SMA
        expected_values = [20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0]

        # Verify results
        self.assertEqual(len(result), len(expected_values))
        np.testing.assert_array_almost_equal(result, expected_values)

    @patch('yfinance.Ticker')
    def test_sma_period_validation(self, mock_ticker):
        # Test that period must be positive
        with self.assertRaises(ValueError):
            MovingAverage(period=0)

        with self.assertRaises(ValueError):
            MovingAverage(period=-1)

    @patch('yfinance.Ticker')
    def test_sma_with_single_value(self, mock_ticker):
        # Setup mock with single value
        single_data = pd.DataFrame({
            'Close': [10]
        }, index=pd.date_range(start='2024-01-01', periods=1))

        mock_ticker_instance = MagicMock()
        mock_ticker_instance.history.return_value = single_data
        mock_ticker.return_value = mock_ticker_instance

        # Test SMA with period 1
        sma = MovingAverage(period=1)
        result = sma.compute(self.mock_stock)

        # Should return empty array as we need at least period number of values
        self.assertEqual(len(result), 0)

    @patch('yfinance.Ticker')
    def test_sma_with_empty_data(self, mock_ticker):
        # Setup mock with empty data
        empty_data = pd.DataFrame({
            'Close': []
        })

        mock_ticker_instance = MagicMock()
        mock_ticker_instance.history.return_value = empty_data
        mock_ticker.return_value = mock_ticker_instance

        # Test SMA with period 3
        sma = MovingAverage(period=3)
        result = sma.compute(self.mock_stock)

        # Should return empty array
        self.assertEqual(len(result), 0)

    @patch('yfinance.Ticker')
    def test_sma_with_different_periods(self, mock_ticker):
        # Setup mock
        mock_ticker_instance = MagicMock()
        mock_ticker_instance.history.return_value = self.sample_data
        mock_ticker.return_value = mock_ticker_instance

        # Test different periods
        periods = [2, 5, 10]
        for period in periods:
            sma = MovingAverage(period=period)
            result = sma.compute(self.mock_stock)

            # Verify length of result
            expected_length = len(self.sample_data) - period + 1
            self.assertEqual(len(result), expected_length)

            # Verify first value is correct
            expected_first = self.sample_data['Close'][:period].mean()
            self.assertAlmostEqual(result[0], expected_first)


if __name__ == '__main__':
    unittest.main()
