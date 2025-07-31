import unittest
import pandas as pd
import numpy as np
from src.strategies import (
    MovingAverageCross, RSICross, RSIExtremes,
    MACDCross, MACDHistogramStrategy, CustomStrategy
)
from src.indicators import SMA, EMA, RSI, MACDLine, MACDSignal, MACDHistogram


class TestStrategyFromParams(unittest.TestCase):

    def test_moving_average_cross_valid_params(self):
        """Test MovingAverageCross creation with valid parameters"""
        # Test SMA type
        params = {
            'lower_period': 5,
            'upper_period': 20,
            'ma_type': 'SMA'
        }
        strategy = MovingAverageCross.generate_from_params(params)

        self.assertEqual(strategy.lower_period, 5)
        self.assertEqual(strategy.upper_period, 20)
        self.assertIsInstance(strategy.lower_ma, SMA)
        self.assertIsInstance(strategy.upper_ma, SMA)

        # Test EMA type
        params = {
            'lower_period': 10,
            'upper_period': 30,
            'ma_type': 'EMA'
        }
        strategy = MovingAverageCross.generate_from_params(params)

        self.assertEqual(strategy.lower_period, 10)
        self.assertEqual(strategy.upper_period, 30)
        self.assertIsInstance(strategy.lower_ma, EMA)
        self.assertIsInstance(strategy.upper_ma, EMA)

    def test_moving_average_cross_string_params(self):
        """Test MovingAverageCross with string parameters (should convert to int)"""
        params = {
            'lower_period': '5',
            'upper_period': '20',
            'ma_type': 'SMA'
        }
        strategy = MovingAverageCross.generate_from_params(params)

        self.assertEqual(strategy.lower_period, 5)
        self.assertEqual(strategy.upper_period, 20)

    def test_moving_average_cross_missing_params(self):
        """Test MovingAverageCross with missing parameters"""
        # Missing lower_period
        params = {
            'upper_period': 20,
            'ma_type': 'SMA'
        }
        with self.assertRaises(ValueError) as context:
            MovingAverageCross.generate_from_params(params)
        self.assertIn("must include", str(context.exception))

        # Missing upper_period
        params = {
            'lower_period': 5,
            'ma_type': 'SMA'
        }
        with self.assertRaises(ValueError) as context:
            MovingAverageCross.generate_from_params(params)
        self.assertIn("must include", str(context.exception))

        # Missing ma_type
        params = {
            'lower_period': 5,
            'upper_period': 20
        }
        with self.assertRaises(ValueError) as context:
            MovingAverageCross.generate_from_params(params)
        self.assertIn("must include", str(context.exception))

    def test_moving_average_cross_invalid_params(self):
        """Test MovingAverageCross with invalid parameter values"""
        # Invalid periods (lower >= upper)
        params = {
            'lower_period': 20,
            'upper_period': 10,
            'ma_type': 'SMA'
        }
        with self.assertRaises(ValueError) as context:
            MovingAverageCross.generate_from_params(params)
        self.assertIn("lower_period must be less than upper_period",
                      str(context.exception))

        # Invalid MA type
        params = {
            'lower_period': 5,
            'upper_period': 20,
            'ma_type': 'INVALID'
        }
        with self.assertRaises(ValueError) as context:
            MovingAverageCross.generate_from_params(params)
        self.assertIn("ma_type must be", str(context.exception))

    def test_rsi_cross_valid_params(self):
        """Test RSICross creation with valid parameters"""
        params = {
            'rsi_period': 14,
            'lower_bound': 30,
            'upper_bound': 70
        }
        strategy = RSICross.generate_from_params(params)

        self.assertEqual(strategy.rsi_period, 14)
        self.assertEqual(strategy.lower_bound, 30)
        self.assertEqual(strategy.upper_bound, 70)
        self.assertIsInstance(strategy.rsi_indicator, RSI)

    def test_rsi_cross_string_params(self):
        """Test RSICross with string parameters"""
        params = {
            'rsi_period': '14',
            'lower_bound': '25',
            'upper_bound': '75'
        }
        strategy = RSICross.generate_from_params(params)

        self.assertEqual(strategy.rsi_period, 14)
        self.assertEqual(strategy.lower_bound, 25)
        self.assertEqual(strategy.upper_bound, 75)

    def test_rsi_cross_missing_params(self):
        """Test RSICross with missing parameters"""
        params = {
            'lower_bound': 30,
            'upper_bound': 70
        }
        with self.assertRaises(ValueError) as context:
            RSICross.generate_from_params(params)
        self.assertIn("must include", str(context.exception))

    def test_rsi_cross_invalid_bounds(self):
        """Test RSICross with invalid bounds"""
        # Lower bound >= upper bound
        params = {
            'rsi_period': 14,
            'lower_bound': 70,
            'upper_bound': 30
        }
        with self.assertRaises(ValueError) as context:
            RSICross.generate_from_params(params)
        self.assertIn("0 < lower_bound < upper_bound < 100",
                      str(context.exception))

    def test_rsi_extremes_valid_params(self):
        """Test RSIExtremes creation with valid parameters"""
        params = {
            'rsi_period': 14,
            'oversold_threshold': 25,
            'overbought_threshold': 75
        }
        strategy = RSIExtremes.generate_from_params(params)

        self.assertEqual(strategy.rsi_period, 14)
        self.assertEqual(strategy.oversold_threshold, 25)
        self.assertEqual(strategy.overbought_threshold, 75)
        self.assertIsInstance(strategy.rsi_indicator, RSI)

    def test_rsi_extremes_missing_params(self):
        """Test RSIExtremes with missing parameters"""
        params = {
            'oversold_threshold': 30,
            'overbought_threshold': 70
        }
        with self.assertRaises(ValueError) as context:
            RSIExtremes.generate_from_params(params)
        self.assertIn("must include", str(context.exception))

    def test_rsi_extremes_invalid_thresholds(self):
        """Test RSIExtremes with invalid thresholds"""
        # Oversold >= overbought
        params = {
            'rsi_period': 14,
            'oversold_threshold': 70,
            'overbought_threshold': 30
        }
        with self.assertRaises(ValueError) as context:
            RSIExtremes.generate_from_params(params)
        self.assertIn("0 < oversold < overbought < 100",
                      str(context.exception))

    def test_macd_cross_valid_params(self):
        """Test MACDCross creation with valid parameters"""
        params = {
            'short_period': 12,
            'long_period': 26,
            'signal_period': 9
        }
        strategy = MACDCross.generate_from_params(params)

        self.assertEqual(strategy.short_period, 12)
        self.assertEqual(strategy.long_period, 26)
        self.assertEqual(strategy.signal_period, 9)
        self.assertIsInstance(strategy.macd_line, MACDLine)
        self.assertIsInstance(strategy.macd_signal, MACDSignal)

    def test_macd_cross_string_params(self):
        """Test MACDCross with string parameters"""
        params = {
            'short_period': '10',
            'long_period': '20',
            'signal_period': '5'
        }
        strategy = MACDCross.generate_from_params(params)

        self.assertEqual(strategy.short_period, 10)
        self.assertEqual(strategy.long_period, 20)
        self.assertEqual(strategy.signal_period, 5)

    def test_macd_cross_missing_params(self):
        """Test MACDCross with missing parameters"""
        params = {
            'short_period': 12,
            'long_period': 26
            # Missing signal_period
        }
        with self.assertRaises(ValueError) as context:
            MACDCross.generate_from_params(params)
        self.assertIn("must include", str(context.exception))

    def test_macd_cross_invalid_periods(self):
        """Test MACDCross with invalid periods"""
        # Short period >= long period
        params = {
            'short_period': 26,
            'long_period': 12,
            'signal_period': 9
        }
        with self.assertRaises(ValueError) as context:
            MACDCross.generate_from_params(params)
        self.assertIn("Short period must be less than long period",
                      str(context.exception))

    def test_macd_histogram_valid_params(self):
        """Test MACDHistogramStrategy creation with valid parameters"""
        params = {
            'short_period': 12,
            'long_period': 26,
            'signal_period': 9
        }
        strategy = MACDHistogramStrategy.generate_from_params(params)

        self.assertEqual(strategy.short_period, 12)
        self.assertEqual(strategy.long_period, 26)
        self.assertEqual(strategy.signal_period, 9)
        self.assertIsInstance(strategy.macd_histogram, MACDHistogram)

    def test_macd_histogram_missing_params(self):
        """Test MACDHistogramStrategy with missing parameters"""
        params = {
            'short_period': 12
            # Missing long_period and signal_period
        }
        with self.assertRaises(ValueError) as context:
            MACDHistogramStrategy.generate_from_params(params)
        self.assertIn("must include", str(context.exception))

    def test_custom_strategy_valid_params(self):
        """Test CustomStrategy creation with valid parameters"""
        # Test all valid modes
        for mode in ['all', 'any', 'majority']:
            params = {'mode': mode}
            strategy = CustomStrategy.generate_from_params(params)
            self.assertEqual(strategy.mode, mode)
            self.assertEqual(len(strategy.strategies), 0)

    def test_custom_strategy_missing_params(self):
        """Test CustomStrategy with missing parameters"""
        params = {}  # Missing mode
        with self.assertRaises(ValueError) as context:
            CustomStrategy.generate_from_params(params)
        self.assertIn("must include 'mode'", str(context.exception))

    def test_custom_strategy_invalid_mode(self):
        """Test CustomStrategy with invalid mode"""
        params = {'mode': 'invalid_mode'}
        with self.assertRaises(ValueError) as context:
            CustomStrategy.generate_from_params(params)
        self.assertIn("mode must be either", str(context.exception))

    def test_all_strategies_return_correct_type(self):
        """Test that all strategies return the correct type"""
        # MovingAverageCross
        params = {'lower_period': 5, 'upper_period': 20, 'ma_type': 'SMA'}
        strategy = MovingAverageCross.generate_from_params(params)
        self.assertIsInstance(strategy, MovingAverageCross)

        # RSICross
        params = {'rsi_period': 14, 'lower_bound': 30, 'upper_bound': 70}
        strategy = RSICross.generate_from_params(params)
        self.assertIsInstance(strategy, RSICross)

        # RSIExtremes
        params = {'rsi_period': 14, 'oversold_threshold': 30,
                  'overbought_threshold': 70}
        strategy = RSIExtremes.generate_from_params(params)
        self.assertIsInstance(strategy, RSIExtremes)

        # MACDCross
        params = {'short_period': 12, 'long_period': 26, 'signal_period': 9}
        strategy = MACDCross.generate_from_params(params)
        self.assertIsInstance(strategy, MACDCross)

        # MACDHistogramStrategy
        params = {'short_period': 12, 'long_period': 26, 'signal_period': 9}
        strategy = MACDHistogramStrategy.generate_from_params(params)
        self.assertIsInstance(strategy, MACDHistogramStrategy)

        # CustomStrategy
        params = {'mode': 'all'}
        strategy = CustomStrategy.generate_from_params(params)
        self.assertIsInstance(strategy, CustomStrategy)

    def test_strategies_have_required_indicators(self):
        """Test that strategies created from params have proper required indicators"""
        # MovingAverageCross
        params = {'lower_period': 5, 'upper_period': 20, 'ma_type': 'SMA'}
        strategy = MovingAverageCross.generate_from_params(params)
        indicators = strategy.get_required_indicators()
        self.assertEqual(len(indicators), 2)
        self.assertTrue(all(hasattr(ind, 'compute') for ind in indicators))

        # RSICross
        params = {'rsi_period': 14, 'lower_bound': 30, 'upper_bound': 70}
        strategy = RSICross.generate_from_params(params)
        indicators = strategy.get_required_indicators()
        self.assertEqual(len(indicators), 1)
        self.assertIsInstance(indicators[0], RSI)

        # MACDCross
        params = {'short_period': 12, 'long_period': 26, 'signal_period': 9}
        strategy = MACDCross.generate_from_params(params)
        indicators = strategy.get_required_indicators()
        self.assertEqual(len(indicators), 2)


if __name__ == '__main__':
    unittest.main()
