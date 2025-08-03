import type { StrategyConfig } from "../utils/types";


interface StrategyCardProps {
    strategy: StrategyConfig;
    handleRemove: (strategy: StrategyConfig) => void;
}

export default function StrategyCard({ strategy, handleRemove }: StrategyCardProps) {
  return (
    <div className="bg-white rounded-lg shadow-lg hover:shadow-xl transition-shadow duration-300 p-6 border border-gray-100">
      <div className="mb-4 flex justify-between items-start">
        <h3 className="text-xl font-semibold text-gray-800 mb-2">
          {strategy.name || 'Strategy'}
        </h3>
        <button
          onClick={() => handleRemove(strategy)}
          className="text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-full p-2 transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-red-100 cursor-pointer"
          aria-label="Delete strategy"
        >
          <span className="text-xl font-bold">&times;</span>
        </button>
      </div>
      <div className="space-y-3">
        {Object.entries(strategy).map(([key, value]) => {
          if (key !== "id" && key !== "name") {
            return (
              <div key={key} className="flex justify-between items-center py-2 border-b border-gray-50 last:border-b-0">
                <span className="text-sm font-medium text-gray-600 capitalize">
                  {key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}:
                </span>
                <span className="text-sm text-gray-900 font-medium bg-gray-50 px-3 py-1 rounded-full">
                  {String(value)}
                </span>
              </div>
            );
          }
        })}
      </div>
    </div>
  );
}