from src.strategies import CustomStrategy, MovingAverageCross, RSICross, RSIExtremes
from backend.models import StrategyConfig
from backend.create_strategy import create_strategy, strategy_mapping
import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the backend directory to the path so we can import from it
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))


class TestCreateStrategy(unittest.TestCase):

    def test_create_strategy_single_moving_average_cross(self):
        """Test creating strategy with single MovingAverageCross"""
        strategy_config = StrategyConfig(
            type="moving_average_cross",
            params={
                'lower_period': 5,
                'upper_period': 20,
                'ma_type': 'SMA'
            }
        )

        result = create_strategy([strategy_config])

        # Should return CustomStrategy
        self.assertIsInstance(result, CustomStrategy)
        self.assertEqual(result.mode, "any")
        self.assertEqual(len(result.strategies), 1)
        self.assertIsInstance(result.strategies[0], MovingAverageCross)

        # Check the strategy was configured correctly
        ma_strategy = result.strategies[0]
        self.assertEqual(ma_strategy.lower_period, 5)
        self.assertEqual(ma_strategy.upper_period, 20)

    def test_create_strategy_single_rsi_extremes(self):
        """Test creating strategy with single RSIExtremes"""
        strategy_config = StrategyConfig(
            type="rsi_extremes",
            params={
                'rsi_period': 14,
                'oversold_threshold': 30,
                'overbought_threshold': 70
            }
        )

        result = create_strategy([strategy_config])

        self.assertIsInstance(result, CustomStrategy)
        self.assertEqual(len(result.strategies), 1)
        self.assertIsInstance(result.strategies[0], RSIExtremes)

        # Check the strategy was configured correctly
        rsi_strategy = result.strategies[0]
        self.assertEqual(rsi_strategy.rsi_period, 14)
        self.assertEqual(rsi_strategy.oversold_threshold, 30)
        self.assertEqual(rsi_strategy.overbought_threshold, 70)

    def test_create_strategy_single_rsi_cross(self):
        """Test creating strategy with single RSICross"""
        strategy_config = StrategyConfig(
            type="rsi_cross",
            params={
                'rsi_period': 14,
                'lower_bound': 30,
                'upper_bound': 70
            }
        )

        result = create_strategy([strategy_config])

        self.assertIsInstance(result, CustomStrategy)
        self.assertEqual(len(result.strategies), 1)
        self.assertIsInstance(result.strategies[0], RSICross)

        # Check the strategy was configured correctly
        rsi_strategy = result.strategies[0]
        self.assertEqual(rsi_strategy.rsi_period, 14)
        self.assertEqual(rsi_strategy.lower_bound, 30)
        self.assertEqual(rsi_strategy.upper_bound, 70)

    def test_create_strategy_multiple_strategies(self):
        """Test creating strategy with multiple different strategies"""
        strategy_configs = [
            StrategyConfig(
                type="moving_average_cross",
                params={
                    'lower_period': 5,
                    'upper_period': 20,
                    'ma_type': 'SMA'
                }
            ),
            StrategyConfig(
                type="rsi_extremes",
                params={
                    'rsi_period': 14,
                    'oversold_threshold': 30,
                    'overbought_threshold': 70
                }
            ),
            StrategyConfig(
                type="rsi_cross",
                params={
                    'rsi_period': 21,
                    'lower_bound': 25,
                    'upper_bound': 75
                }
            )
        ]

        result = create_strategy(strategy_configs)

        self.assertIsInstance(result, CustomStrategy)
        self.assertEqual(result.mode, "any")
        self.assertEqual(len(result.strategies), 3)

        # Check each strategy type
        self.assertIsInstance(result.strategies[0], MovingAverageCross)
        self.assertIsInstance(result.strategies[1], RSIExtremes)
        self.assertIsInstance(result.strategies[2], RSICross)

        # Check specific parameters
        self.assertEqual(result.strategies[0].lower_period, 5)
        self.assertEqual(result.strategies[1].rsi_period, 14)
        self.assertEqual(result.strategies[2].lower_bound, 25)

    def test_create_strategy_empty_list(self):
        """Test creating strategy with empty strategy list"""
        result = create_strategy([])

        self.assertIsInstance(result, CustomStrategy)
        self.assertEqual(result.mode, "any")
        self.assertEqual(len(result.strategies), 0)

    def test_create_strategy_invalid_strategy_type(self):
        """Test creating strategy with invalid strategy type"""
        strategy_config = StrategyConfig(
            type="moving_average_cross",  # This will be overridden
            params={'some': 'params'}
        )
        # Manually set an invalid type to test error handling
        strategy_config.type = "invalid_strategy_type"

        with self.assertRaises(ValueError) as context:
            create_strategy([strategy_config])

        self.assertIn("Strategy not yet implemented!", str(context.exception))

    def test_create_strategy_invalid_params(self):
        """Test creating strategy with invalid parameters"""
        # Test with missing required parameters
        strategy_config = StrategyConfig(
            type="moving_average_cross",
            params={
                'lower_period': 5,
                # Missing upper_period and ma_type
            }
        )

        with self.assertRaises(ValueError):
            create_strategy([strategy_config])

        # Test with invalid parameter values
        strategy_config = StrategyConfig(
            type="moving_average_cross",
            params={
                'lower_period': 20,  # Invalid: lower >= upper
                'upper_period': 10,
                'ma_type': 'SMA'
            }
        )

        with self.assertRaises(ValueError):
            create_strategy([strategy_config])

    def test_create_strategy_string_params(self):
        """Test creating strategy with string parameters (should convert to int)"""
        strategy_config = StrategyConfig(
            type="moving_average_cross",
            params={
                'lower_period': '5',  # String values
                'upper_period': '20',
                'ma_type': 'SMA'
            }
        )

        result = create_strategy([strategy_config])

        self.assertIsInstance(result, CustomStrategy)
        self.assertEqual(len(result.strategies), 1)

        # Check the strategy was configured correctly with converted values
        ma_strategy = result.strategies[0]
        self.assertEqual(ma_strategy.lower_period, 5)
        self.assertEqual(ma_strategy.upper_period, 20)

    def test_create_strategy_duplicate_strategy_types(self):
        """Test creating strategy with multiple instances of same strategy type"""
        strategy_configs = [
            StrategyConfig(
                type="moving_average_cross",
                params={
                    'lower_period': 5,
                    'upper_period': 20,
                    'ma_type': 'SMA'
                }
            ),
            StrategyConfig(
                type="moving_average_cross",
                params={
                    'lower_period': 10,
                    'upper_period': 30,
                    'ma_type': 'EMA'
                }
            )
        ]

        result = create_strategy(strategy_configs)

        self.assertIsInstance(result, CustomStrategy)
        self.assertEqual(len(result.strategies), 2)
        self.assertIsInstance(result.strategies[0], MovingAverageCross)
        self.assertIsInstance(result.strategies[1], MovingAverageCross)

        # Check they have different parameters
        self.assertEqual(result.strategies[0].lower_period, 5)
        self.assertEqual(result.strategies[1].lower_period, 10)

    def test_strategy_mapping_contains_expected_strategies(self):
        """Test that strategy_mapping contains the expected strategy types"""
        expected_strategies = {
            "moving_average_cross": MovingAverageCross,
            "rsi_extremes": RSIExtremes,
            "rsi_cross": RSICross
        }

        self.assertEqual(strategy_mapping, expected_strategies)

    def test_create_strategy_with_all_strategy_types(self):
        """Test creating strategy using all available strategy types"""
        strategy_configs = []

        # Add one of each strategy type
        for strategy_type in strategy_mapping.keys():
            if strategy_type == "moving_average_cross":
                params = {
                    'lower_period': 5,
                    'upper_period': 20,
                    'ma_type': 'SMA'
                }
            elif strategy_type == "rsi_extremes":
                params = {
                    'rsi_period': 14,
                    'oversold_threshold': 30,
                    'overbought_threshold': 70
                }
            elif strategy_type == "rsi_cross":
                params = {
                    'rsi_period': 14,
                    'lower_bound': 30,
                    'upper_bound': 70
                }

            strategy_configs.append(StrategyConfig(
                type=strategy_type,
                params=params
            ))

        result = create_strategy(strategy_configs)

        self.assertIsInstance(result, CustomStrategy)
        self.assertEqual(len(result.strategies), len(strategy_mapping))

        # Verify each strategy type is present
        strategy_types = [type(s).__name__ for s in result.strategies]
        expected_types = [cls.__name__ for cls in strategy_mapping.values()]

        for expected_type in expected_types:
            self.assertIn(expected_type, strategy_types)

    def test_create_strategy_preserves_order(self):
        """Test that strategies are added in the same order as provided"""
        strategy_configs = [
            StrategyConfig(type="rsi_cross", params={
                'rsi_period': 14, 'lower_bound': 30, 'upper_bound': 70
            }),
            StrategyConfig(type="moving_average_cross", params={
                'lower_period': 5, 'upper_period': 20, 'ma_type': 'SMA'
            }),
            StrategyConfig(type="rsi_extremes", params={
                'rsi_period': 14, 'oversold_threshold': 30, 'overbought_threshold': 70
            })
        ]

        result = create_strategy(strategy_configs)

        # Check the order is preserved
        self.assertIsInstance(result.strategies[0], RSICross)
        self.assertIsInstance(result.strategies[1], MovingAverageCross)
        self.assertIsInstance(result.strategies[2], RSIExtremes)

    def test_create_strategy_returns_custom_strategy_with_any_mode(self):
        """Test that the returned CustomStrategy always has mode 'any'"""
        strategy_config = StrategyConfig(
            type="moving_average_cross",
            params={
                'lower_period': 5,
                'upper_period': 20,
                'ma_type': 'SMA'
            }
        )

        result = create_strategy([strategy_config])

        self.assertIsInstance(result, CustomStrategy)
        self.assertEqual(result.mode, "any")


if __name__ == '__main__':
    unittest.main()
