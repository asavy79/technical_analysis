import React from "react";
import { strategyRegistry, type StrategyConfig } from "../utils/types";

type Props = {
  strategy: StrategyConfig;
  onChange: (updated: StrategyConfig) => void;
  onSubmit: (event: React.FormEvent) => void;
};

export const StrategyForm: React.FC<Props> = ({
  strategy,
  onChange,
  onSubmit,
}) => {
  const meta = strategyRegistry[strategy.name];

  const handleChange = (key: string, value: string | number) => {
    const updated = { ...strategy, [key]: value };
    onChange(updated as StrategyConfig);
  };

  return (
    <form className="bg-white dark:bg-gray-900 p-6 rounded-2xl shadow-md space-y-6 max-w-md mx-auto">
      <h3 className="text-2xl font-semibold text-gray-800 dark:text-white">
        {meta.label}
      </h3>

      {Object.entries(meta.fields).map(([key, config]) => {
        const value = strategy[key as keyof typeof strategy];

        return (
          <div key={key} className="flex flex-col space-y-2">
            <label className="text-sm font-medium text-gray-700 dark:text-gray-300">
              {config.label}
            </label>

            {config.type === "select" ? (
              <select
                value={value as string}
                onChange={(e) => handleChange(key, e.target.value)}
                className="rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-white px-4 py-2 shadow-sm focus:ring-2 focus:ring-indigo-500 focus:outline-none"
              >
                {config.options?.map((opt) => (
                  <option key={opt} value={opt}>
                    {opt}
                  </option>
                ))}
              </select>
            ) : (
              <input
                type={config.type}
                value={value as string | number}
                onChange={(e) =>
                  handleChange(
                    key,
                    config.type === "number"
                      ? Number(e.target.value)
                      : e.target.value
                  )
                }
                className="rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-white px-4 py-2 shadow-sm focus:ring-2 focus:ring-indigo-500 focus:outline-none"
              />
            )}
          </div>
        );
      })}
      <button
        className="bg-blue-500 text-white p-3 rounded-lg"
        onClick={onSubmit}
      >
        Add Strategy
      </button>
    </form>
  );
};
