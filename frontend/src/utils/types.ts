type FieldType = "number" | "text" | "select";

type FieldConfig = {
  label: string;
  type: FieldType;
  options?: string[]; // for select fields
};

type StrategyMeta = {
  label: string;
  fields: {
    [fieldName: string]: FieldConfig;
  };
};

export const strategyRegistry: Record<string, StrategyMeta> = {
  "RSI Extremes": {
    label: "RSI Extremes",
    fields: {
      rsi_period: { label: "RSI Period", type: "number" },
      overbought_threshold: { label: "Overbought Threshold", type: "number" },
      oversold_threshold: { label: "Oversold Threshold", type: "number" },
    },
  },
  "Moving Average Cross": {
    label: "Moving Average Cross",
    fields: {
      lower_period: { label: "Lower Period", type: "number" },
      upper_period: { label: "Upper Period", type: "number" },
      ma_type: {
        label: "MA Type",
        type: "select",
        options: ["SMA", "EMA"],
      },
    },
  },
  "MACD Cross": {
    label: "MACD Cross",
    fields: {
      short_period: {label: "Short Period", type: "number"},
      long_period: {label: "Long Period", type: "number"},
      signal_period: {label: "Signal Period", type: "number"}
    }
  }
};


type RSIStrategy = {
  name: "RSI Extremes";
  id: string;
  rsi_period: number;
  overbought_threshold: number;
  oversold_threshold: number;
};

type MAStrategy = {
  name: "Moving Average Cross";
  id: string;
  lower_period: number;
  upper_period: number;
  ma_type: string;
};

type MACDStrategy = {
  name: "MACD Cross",
  id: string;
  short_period: number;
  long_period: number;
  signal_period: number;
}

export type StrategyConfig = RSIStrategy | MAStrategy | MACDStrategy;



export type RawTrades = {
  entry_date: Record<string, string>;
  exit_date: Record<string, string>;
  entry_price: Record<string, number>;
  exit_price: Record<string, number>;
  return: Record<string, number>;
  duration: Record<string, number>;
};


export type FormattedTrade = {
  entry_date: string;
  exit_date: string;
  entry_price: number;
  exit_price: number;
  return: number;
  duration: number;
};

export type Trade = {
  entry_date: string;
  exit_date: string;
  entry_price: number;
  exit_price: number;
  return: number;
  duration: number;
};

export type BacktestResult = {
  total_return: number;
  total_trades: number;
  winning_trades: number;
  losing_trades: number;
  win_rate: number;
  avg_return_per_trade: number;
  avg_winning_trade: number;
  avg_losing_trade: number;
  max_drawdown: number;
  sharpe_ratio: number;
  final_capital: number;
  trades: Trade[];
};

