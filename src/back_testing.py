import pandas as pd
import numpy as np
from typing import Dict, Tuple


class BackTest:
    def __init__(self, initial_capital: float = 10000):
        if initial_capital <= 0:
            raise ValueError("Initial capital must be positive")
        self.initial_capital = initial_capital

    def run_backtest(self, market_data, strategy) -> Dict:
        # Check for all required columns and whatnot
        strategy.validate_data(market_data)

        signals = strategy.calculate_signals(market_data)

        price_data = market_data.get_raw_data()['Close']

        trades = self._generate_trades(signals, price_data)

        metrics = self._calculate_metrics(trades, price_data)

        return {
            'trades': trades,
            'metrics': metrics,
            'signals': signals
        }

    def _generate_trades(self, signals: Dict[str, pd.Series], prices: pd.Series) -> pd.DataFrame:
        buy_signals = signals['buy']
        sell_signals = signals['sell']

        # Align signals with prices
        buy_signals = buy_signals.reindex(prices.index, fill_value=False)
        sell_signals = sell_signals.reindex(prices.index, fill_value=False)

        trades = []
        position = 0  # 0 = no position, 1 = long position
        entry_price = None
        entry_date = None

        for date in prices.index:
            price = prices[date]

            # need to make sure you're not already in a position
            if buy_signals[date] and position == 0:
                position = 1
                entry_price = price
                entry_date = date

            # Before selling you need to be in a long position
            elif sell_signals[date] and position == 1:
                exit_price = price
                exit_date = date

                # Big W trade
                trade_return = (exit_price - entry_price) / entry_price

                trades.append({
                    'entry_date': entry_date,
                    'exit_date': exit_date,
                    'entry_price': entry_price,
                    'exit_price': exit_price,
                    'return': trade_return,
                    'duration': (exit_date - entry_date).days
                })

                position = 0
                entry_price = None
                entry_date = None

        return pd.DataFrame(trades)

    def _calculate_metrics(self, trades: pd.DataFrame, prices: pd.Series) -> Dict:
        if trades.empty:
            return {
                'total_return': 0.0,
                'total_trades': 0,
                'winning_trades': 0,
                'losing_trades': 0,
                'win_rate': 0.0,
                'avg_return_per_trade': 0.0,
                'avg_winning_trade': 0.0,
                'avg_losing_trade': 0.0,
                'max_drawdown': 0.0,
                'sharpe_ratio': 0.0,
                'final_capital': self.initial_capital,
                'trades': []
            }

        total_trades = len(trades)
        winning_trades = len(trades[trades['return'] > 0])
        losing_trades = len(trades[trades['return'] < 0])
        win_rate = winning_trades / total_trades if total_trades > 0 else 0

        avg_return_per_trade = trades['return'].mean()
        avg_winning_trade = trades[trades['return'] >
                                   0]['return'].mean() if winning_trades > 0 else 0
        avg_losing_trade = trades[trades['return'] <
                                  0]['return'].mean() if losing_trades > 0 else 0

        # Calculate cumulative returns
        cumulative_return = (1 + trades['return']).prod() - 1
        final_capital = self.initial_capital * (1 + cumulative_return)

        # Calculate maximum drawdown
        cumulative_returns = (1 + trades['return']).cumprod()
        running_max = cumulative_returns.expanding().max()
        drawdown = (cumulative_returns - running_max) / running_max
        max_drawdown = drawdown.min()

        # Calculate Sharpe ratio (simplified - assumes daily returns)
        if trades['return'].std() > 0:
            sharpe_ratio = trades['return'].mean(
            ) / trades['return'].std() * np.sqrt(252)  # Annualized
        else:
            sharpe_ratio = 0.0

        trades_arr = trades.to_dict(orient='records')

        return {
            'total_return': cumulative_return,
            'total_trades': total_trades,
            'winning_trades': winning_trades,
            'losing_trades': losing_trades,
            'win_rate': win_rate,
            'avg_return_per_trade': avg_return_per_trade,
            'avg_winning_trade': avg_winning_trade,
            'avg_losing_trade': avg_losing_trade,
            'max_drawdown': max_drawdown,
            'sharpe_ratio': sharpe_ratio,
            'final_capital': final_capital,
            'trades': trades_arr
        }

    def print_results(self, results: Dict):
        """Print formatted backtest results"""
        metrics = results['metrics']
        trades = results['trades']

        print("=" * 50)
        print("BACKTEST RESULTS")
        print("=" * 50)
        print(f"Initial Capital: ${self.initial_capital:,.2f}")
        print(f"Final Capital: ${metrics['final_capital']:,.2f}")
        print(f"Total Return: {metrics['total_return']:.2%}")
        print()
        print(f"Total Trades: {metrics['total_trades']}")
        print(f"Winning Trades: {metrics['winning_trades']}")
        print(f"Losing Trades: {metrics['losing_trades']}")
        print(f"Win Rate: {metrics['win_rate']:.2%}")
        print()
        print(
            f"Average Return per Trade: {metrics['avg_return_per_trade']:.2%}")
        print(f"Average Winning Trade: {metrics['avg_winning_trade']:.2%}")
        print(f"Average Losing Trade: {metrics['avg_losing_trade']:.2%}")
        print()
        print(f"Maximum Drawdown: {metrics['max_drawdown']:.2%}")
        print(f"Sharpe Ratio: {metrics['sharpe_ratio']:.2f}")
        print("=" * 50)

        if not trades.empty:
            print("\nFirst 5 Trades:")
            print(trades.head().to_string(index=False))
            print("\nLast 5 Trades:")
            print(trades.tail().to_string(index=False))
