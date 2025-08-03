import React from "react";
import { strategyRegistry, type StrategyConfig } from "../utils/types";

type Props = {
  strategy: StrategyConfig;
  onChange: (updated: StrategyConfig) => void;
  onSubmit: (event: React.FormEvent) => void;
  onCancel: () => void;
};

export const StrategyForm: React.FC<Props> = ({
  strategy,
  onChange,
  onSubmit,
  onCancel,
}) => {
  const meta = strategyRegistry[strategy.name];

  const handleChange = (key: string, value: string | number) => {
    const updated = { ...strategy, [key]: value };
    onChange(updated as StrategyConfig);
  };

  return (
    <form className="bg-white p-8 rounded-xl shadow-lg border border-gray-100 space-y-6 max-w-lg mx-auto">
      <div className="text-center border-b border-gray-100 pb-4">
        <h3 className="text-2xl font-bold text-gray-800 mb-1">
          {meta.label}
        </h3>
        <p className="text-gray-500 text-sm">Configure your strategy parameters</p>
      </div>

      <div className="space-y-5">
        {Object.entries(meta.fields).map(([key, config]) => {
          const value = strategy[key as keyof typeof strategy];

          return (
            <div key={key} className="space-y-2">
              <label className="block text-sm font-semibold text-gray-700">
                {config.label}
              </label>

              {config.type === "select" ? (
                <select
                  value={value as string}
                  onChange={(e) => handleChange(key, e.target.value)}
                  className="w-full rounded-lg border-2 border-gray-200 bg-white text-gray-900 px-4 py-3 shadow-sm focus:border-blue-500 focus:ring-4 focus:ring-blue-100 transition-all duration-200 outline-none"
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
                  className="w-full rounded-lg border-2 border-gray-200 bg-white text-gray-900 px-4 py-3 shadow-sm focus:border-blue-500 focus:ring-4 focus:ring-blue-100 transition-all duration-200 outline-none placeholder-gray-400"
                  placeholder={`Enter ${config.label.toLowerCase()}`}
                />
              )}
            </div>
          );
        })}
      </div>

      <div className="pt-4 flex justify-between gap-4">
        <button
          type="submit"
          onClick={onSubmit}
          className="w-full bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white font-semibold py-3 px-6 rounded-lg shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition-all duration-200 focus:outline-none focus:ring-4 focus:ring-blue-100 cursor-pointer"
        >
          Add Strategy
        </button>
        <button
          onClick={onCancel}
          className="w-full bg-gradient-to-r from-red-500 to-red-600 hover:from-red-600 hover:to-red-700 text-white font-semibold py-3 px-6 rounded-lg shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition-all duration-200 focus:outline-none focus:ring-4 focus:ring-red-100 cursor-pointer"
        >
          Cancel
        </button>
      </div>
    </form>
  );
};
