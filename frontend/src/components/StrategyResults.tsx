import TradeTable from "./TradeTable";
import { type BacktestResult } from "../utils/types";


export default function StrategyResults({ backtestResults }: { backtestResults: BacktestResult }) {
    const formatCurrency = (value: number) => `$${value.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    const formatPercentage = (value: number) => `${(value * 100).toFixed(2)}%`;
    const formatNumber = (value: number) => value.toFixed(2);

    return (
        <div className="space-y-6">
            <h2 className="text-2xl font-bold text-gray-800 mb-6">Backtest Results</h2>
            
            {/* Performance Metrics Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
                {/* Total Return Card */}
                <div className="bg-white rounded-lg shadow-lg border border-gray-100 p-6">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm font-medium text-gray-600">Total Return</p>
                            <p className={`text-2xl font-bold ${backtestResults.total_return >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                                {backtestResults.total_return >= 0 ? '+' : ''}{formatPercentage(backtestResults.total_return)}
                            </p>
                        </div>
                        <div className={`w-12 h-12 rounded-full flex items-center justify-center ${
                            backtestResults.total_return >= 0 ? 'bg-green-100' : 'bg-red-100'
                        }`}>
                            <span className={`text-xl ${backtestResults.total_return >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                                {backtestResults.total_return >= 0 ? '↗' : '↘'}
                            </span>
                        </div>
                    </div>
                </div>

                {/* Final Capital Card */}
                <div className="bg-white rounded-lg shadow-lg border border-gray-100 p-6">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm font-medium text-gray-600">Final Capital</p>
                            <p className="text-2xl font-bold text-gray-900">
                                {formatCurrency(backtestResults.final_capital)}
                            </p>
                        </div>
                        <div className="w-12 h-12 rounded-full bg-blue-100 flex items-center justify-center">
                            <span className="text-xl text-blue-600">💰</span>
                        </div>
                    </div>
                </div>

                {/* Win Rate Card */}
                <div className="bg-white rounded-lg shadow-lg border border-gray-100 p-6">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm font-medium text-gray-600">Win Rate</p>
                            <p className={`text-2xl font-bold ${backtestResults.win_rate >= 0.5 ? 'text-green-600' : 'text-yellow-600'}`}>
                                {formatPercentage(backtestResults.win_rate)}
                            </p>
                        </div>
                        <div className={`w-12 h-12 rounded-full flex items-center justify-center ${
                            backtestResults.win_rate >= 0.5 ? 'bg-green-100' : 'bg-yellow-100'
                        }`}>
                            <span className={`text-xl ${backtestResults.win_rate >= 0.5 ? 'text-green-600' : 'text-yellow-600'}`}>
                                🎯
                            </span>
                        </div>
                    </div>
                </div>

                {/* Sharpe Ratio Card */}
                <div className="bg-white rounded-lg shadow-lg border border-gray-100 p-6">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm font-medium text-gray-600">Sharpe Ratio</p>
                            <p className={`text-2xl font-bold ${backtestResults.sharpe_ratio >= 1 ? 'text-green-600' : backtestResults.sharpe_ratio >= 0 ? 'text-yellow-600' : 'text-red-600'}`}>
                                {formatNumber(backtestResults.sharpe_ratio)}
                            </p>
                        </div>
                        <div className="w-12 h-12 rounded-full bg-purple-100 flex items-center justify-center">
                            <span className="text-xl text-purple-600">📊</span>
                        </div>
                    </div>
                </div>

                {/* Max Drawdown Card */}
                <div className="bg-white rounded-lg shadow-lg border border-gray-100 p-6">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm font-medium text-gray-600">Max Drawdown</p>
                            <p className="text-2xl font-bold text-red-600">
                                {formatPercentage(backtestResults.max_drawdown)}
                            </p>
                        </div>
                        <div className="w-12 h-12 rounded-full bg-red-100 flex items-center justify-center">
                            <span className="text-xl text-red-600">📉</span>
                        </div>
                    </div>
                </div>

                {/* Total Trades Card */}
                <div className="bg-white rounded-lg shadow-lg border border-gray-100 p-6">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm font-medium text-gray-600">Total Trades</p>
                            <p className="text-2xl font-bold text-gray-900">
                                {backtestResults.total_trades}
                            </p>
                        </div>
                        <div className="w-12 h-12 rounded-full bg-indigo-100 flex items-center justify-center">
                            <span className="text-xl text-indigo-600">🔄</span>
                        </div>
                    </div>
                </div>
            </div>

            {/* Detailed Metrics */}
            <div className="bg-white rounded-lg shadow-lg border border-gray-100 p-6">
                <h3 className="text-lg font-semibold text-gray-800 mb-4">Detailed Metrics</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="space-y-3">
                        <div className="flex justify-between">
                            <span className="text-gray-600">Winning Trades:</span>
                            <span className="font-semibold text-green-600">{backtestResults.winning_trades}</span>
                        </div>
                        <div className="flex justify-between">
                            <span className="text-gray-600">Losing Trades:</span>
                            <span className="font-semibold text-red-600">{backtestResults.losing_trades}</span>
                        </div>
                        <div className="flex justify-between">
                            <span className="text-gray-600">Avg Return per Trade:</span>
                            <span className={`font-semibold ${backtestResults.avg_return_per_trade >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                                {formatPercentage(backtestResults.avg_return_per_trade)}
                            </span>
                        </div>
                    </div>
                    <div className="space-y-3">
                        <div className="flex justify-between">
                            <span className="text-gray-600">Avg Winning Trade:</span>
                            <span className="font-semibold text-green-600">{formatPercentage(backtestResults.avg_winning_trade)}</span>
                        </div>
                        <div className="flex justify-between">
                            <span className="text-gray-600">Avg Losing Trade:</span>
                            <span className="font-semibold text-red-600">{formatPercentage(backtestResults.avg_losing_trade)}</span>
                        </div>
                    </div>
                </div>
            </div>

            {/* Trade Table */}
            <TradeTable trades={backtestResults.trades} />
        </div>
    )
}