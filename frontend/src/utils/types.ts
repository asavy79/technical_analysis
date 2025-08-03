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
  
export type StrategyConfig = RSIStrategy | MAStrategy;
  