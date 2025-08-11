import { StrategyForm } from "./EditStrategy";
import { useState } from "react";
import type { StrategyConfig } from "../utils/types";
import { strategyRegistry } from "../utils/types";
import * as React from "react";

// Define default parameters per strategy
const defaultStrategies: Record<StrategyConfig["name"], StrategyConfig> = {
  "RSI Extremes": {
    name: "RSI Extremes",
    id: "rsi_extremes",
    rsi_period: 14,
    overbought_threshold: 70,
    oversold_threshold: 30,
  },
  "Moving Average Cross": {
    name: "Moving Average Cross",
    id: "moving_average_cross",
    lower_period: 50,
    upper_period: 200,
    ma_type: "SMA",
  },
  "MACD Cross": {
    name: "MACD Cross",
    id: "macd_cross",
    short_period: 12,
    long_period: 26,
    signal_period: 9,
  },
};

export default function AddStrategy({
  onAddStrategy,
  onCancel,
}: {
  onAddStrategy: (strategy: StrategyConfig) => void;
  onCancel: () => void;
}) {
  const [strategy, setStrategy] = useState<StrategyConfig>(
    defaultStrategies["RSI Extremes"]
  );

  const onSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    onAddStrategy(strategy);
  };

  return (
    <div className="max-w-xl mx-auto p-8 space-y-6">
      <div className="space-y-2">
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
          Select Strategy
        </label>
        <select
          value={strategy.name}
          onChange={(e) =>
            setStrategy(
              defaultStrategies[e.target.value as StrategyConfig["name"]]
            )
          }
          className="w-full rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-white px-4 py-2 shadow-sm focus:ring-2 focus:ring-indigo-500 focus:outline-none"
        >
          {Object.keys(defaultStrategies).map((strategyName) => (
            <option key={strategyName} value={strategyName}>
              {strategyRegistry[strategyName].label}
            </option>
          ))}
        </select>
      </div>

      <StrategyForm
        strategy={strategy}
        onChange={setStrategy}
        onSubmit={onSubmit}
        onCancel={onCancel}
      />
    </div>
  );
}
