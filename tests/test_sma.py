import unittest
import pandas as pd
import numpy as np
from src.indicators import SMA
from src.main import MarketData
from unittest.mock import patch, MagicMock


class TestSMA(unittest.TestCase):
    def setUp(self):
        # Create sample data for testing
        self.sample_data = pd.DataFrame({
            'Open': [10, 15, 20, 25, 30, 35, 40, 45, 50, 55],
            'High': [12, 17, 22, 27, 32, 37, 42, 47, 52, 57],
            'Low': [8, 13, 18, 23, 28, 33, 38, 43, 48, 53],
            'Close': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
            'Volume': [1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900]
        }, index=pd.date_range(start='2024-01-01', periods=10))

    def test_sma_calculation(self):
        # Test SMA with period 3
        sma = SMA(period=3)
        result = sma.compute(self.sample_data)

        # Expected values for 3-period SMA
        # Day 1-2: NaN (not enough data)
        # Day 3: (10+20+30)/3 = 20
        # Day 4: (20+30+40)/3 = 30
        # Day 5: (30+40+50)/3 = 40
        # etc.
        expected_values = [np.nan, np.nan, 20.0,
                           30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0]

        # Verify results (ignoring NaN values)
        np.testing.assert_array_almost_equal(result.values, expected_values)

    def test_sma_period_validation(self):
        # Test that period must be positive
        with self.assertRaises(ValueError):
            SMA(period=0)

        with self.assertRaises(ValueError):
            SMA(period=-1)

    def test_sma_missing_close_column(self):
        # Test with data missing Close column
        bad_data = pd.DataFrame({
            'Open': [10, 20, 30],
            'High': [12, 22, 32]
        })

        sma = SMA(period=2)
        with self.assertRaises(ValueError) as context:
            sma.compute(bad_data)

        self.assertIn("Close column required", str(context.exception))

    def test_sma_insufficient_data(self):
        # Test with insufficient data points
        small_data = pd.DataFrame({
            'Close': [10, 20]
        })

        sma = SMA(period=5)
        with self.assertRaises(ValueError) as context:
            sma.compute(small_data)

        self.assertIn("Not enough data points", str(context.exception))

    def test_sma_with_different_periods(self):
        # Test different periods
        periods = [1, 2, 5]
        for period in periods:
            sma = SMA(period=period)
            result = sma.compute(self.sample_data)

            # Verify length of result matches input data
            self.assertEqual(len(result), len(self.sample_data))

            # Verify first non-NaN value is correct
            first_valid_idx = period - 1
            expected_first = self.sample_data['Close'][:period].mean()
            self.assertAlmostEqual(
                result.iloc[first_valid_idx], expected_first)

    def test_sma_string_representation(self):
        # Test string representation for caching
        sma_20 = SMA(20)
        sma_50 = SMA(50)

        self.assertEqual(str(sma_20), "SMA_20")
        self.assertEqual(str(sma_50), "SMA_50")

        # Test equality and hashing
        sma_20_copy = SMA(20)
        self.assertEqual(sma_20, sma_20_copy)
        self.assertEqual(hash(sma_20), hash(sma_20_copy))
        self.assertNotEqual(sma_20, sma_50)

    @patch('yfinance.Ticker')
    def test_integration_with_market_data(self, mock_ticker):
        # Test SMA integration with MarketData class
        mock_ticker_instance = MagicMock()
        mock_ticker_instance.history.return_value = self.sample_data
        mock_ticker.return_value = mock_ticker_instance

        # Create MarketData instance
        market_data = MarketData("AAPL", "10d")

        # Create SMA indicator
        sma = SMA(period=3)

        # Get indicator data (should be cached)
        result1 = market_data.get_indicator_data(sma)
        result2 = market_data.get_indicator_data(sma)

        # Should be the same object (cached)
        self.assertTrue(result1.equals(result2))

        # Verify cache contains the indicator
        self.assertIn("SMA_3", market_data._indicator_cache)


if __name__ == '__main__':
    unittest.main()
