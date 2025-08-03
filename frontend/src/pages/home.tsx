import { useState } from "react";
import type { StrategyConfig } from "../utils/types";
import AddStrategy from "../components/AddStrategy";
import StrategyCard from "../components/StrategyCard";
import { testStrategy } from "../services/strategies";
import { type BacktestResult} from "../utils/types";
import StrategyResults from "../components/StrategyResults";
import { validateInput } from "../utils/helpers";




export default function Home() {

  const [ticker, setTicker] = useState<string>("");
  const [strategies, setStrategies] = useState<StrategyConfig[]>([]);

  const [strategyIdSet, setStrategyIdSet] = useState<Set<string>>(new Set());

  const [isAddingStrategy, setIsAddingStrategy] = useState(false);

  const [initialCapital, setInitialCapital] = useState<number>(10000);
  const [period, setPeriod] = useState<string>("1y");

  const [rawData, setRawData] = useState<BacktestResult | null>(null);

  const [error, setError] = useState("");

  const handleTestStrategy = async () => {
    setError("");
    setRawData(null);

    const validationResult = validateInput(strategies, ticker, initialCapital, period);

    if (!validationResult.success) {
      setError(validationResult.error);
      return;
    }

    const result = await testStrategy(strategies, ticker, initialCapital, period);

    if(!result.success) {
      setError("Invalid input. Please try again.");
      return;
    }

    setRawData(result.data);
  }

  const handleAddStrategy = (strategy: StrategyConfig) => {
    if (strategyIdSet.has(strategy.id)) {
      return;
    }
    setStrategyIdSet(new Set([...strategyIdSet, strategy.id]));
    setStrategies([...strategies, strategy]);
    setIsAddingStrategy(false);
  }

  const handleRemoveStrategy = (strategy: StrategyConfig) => {
    setStrategies(strategies.filter((s) => s.id !== strategy.id));
    setStrategyIdSet(new Set([...Array.from(strategyIdSet).filter((id) => id !== strategy.id)]));
  }


  return (
    <div className="max-w-6xl mx-auto p-8 space-y-6">
      <div className="space-y-4">
        <h1 className="text-2xl font-bold">Strategies</h1>
        {strategies.map((strategy) => (
          <StrategyCard key={strategy.id} strategy={strategy} handleRemove={handleRemoveStrategy} />
        ))}
      </div>

      {isAddingStrategy ? (
        <div className="fixed inset-0 bg-opacity-50 items-center">
          <AddStrategy onAddStrategy={handleAddStrategy} onCancel={() => setIsAddingStrategy(false)} />
        </div>
      ) : (
        <div className="flex justify-center">
          <button className="bg-blue-500 text-white p-3 rounded-lg cursor-pointer" onClick={() => setIsAddingStrategy(true)}>
            Add Strategy
          </button>
        </div>
      )}

      <div className="flex justify-between items-center">
        <input type="text" value={ticker} onChange={(e) => setTicker(e.target.value)} className="w-full rounded-lg border border-gray-300 bg-white text-gray-900 px-4 py-2 shadow-sm focus:ring-2 focus:ring-indigo-500 focus:outline-none" placeholder="Enter ticker" />
      </div>

      <div className="flex flex-col justify-between items-center">
        <label htmlFor="initialCapital">Initial Capital</label>
        <input type="number" value={initialCapital} onChange={(e) => setInitialCapital(Number(e.target.value))} className="w-full rounded-lg border border-gray-300 bg-white text-gray-900 px-4 py-2 shadow-sm focus:ring-2 focus:ring-indigo-500 focus:outline-none" placeholder="Enter initial capital" />
      </div>

      <div className="flex flex-col justify-between items-center">
        <label htmlFor="period">Period</label>
        <input type="text" value={period} onChange={(e) => setPeriod(e.target.value)} className="w-full rounded-lg border border-gray-300 bg-white text-gray-900 px-4 py-2 shadow-sm focus:ring-2 focus:ring-indigo-500 focus:outline-none" placeholder="Enter period" />
      </div>

      <div className="flex flex-col justify-between items-center">
        <button className="bg-blue-500 text-white p-3 rounded-lg cursor-pointer" onClick={handleTestStrategy}>
          Test Strategy
        </button>
      </div>

      {error && <div className="text-red-500">{error}</div>}

      <div className="mt-8">
        {rawData && <StrategyResults backtestResults={rawData} />}
      </div>

    </div>
  );
}
