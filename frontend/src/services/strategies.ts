import axios from "./api";
import type { StrategyConfig } from "../utils/types";


const formatStrategyParams = (strategies: StrategyConfig[]) => {
  return strategies.map((strategy) => {
    return {
      type: strategy.id,
      params: {
        ...strategy,
      }
    };
  });
};

export type StrategyMetadata = {
  [key: string]: {
    label: string;
    params: {
      [param: string]: {
        type: string;
      };
    };
  };
};


export async function testStrategy(strategies: StrategyConfig[], ticker: string, initial_capital: number, period: string) {
  try {
    const result = await axios.post("/backtest", { strategies: formatStrategyParams(strategies), ticker, initial_capital: String(initial_capital), period });
    console.log(result.data);
    return {
      success: true,
      data: result.data,
    };
  } catch (error) {
    console.error("Error testing strategy:", error);
    return {
      success: false,
      data: null,
      error: error instanceof Error ? error.message : "Unknown error",
    };
  }
}
