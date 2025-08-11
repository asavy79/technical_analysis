import { type RawTrades, type FormattedTrade, type StrategyConfig } from "./types";


export function formatTrades(trades: RawTrades): FormattedTrade[] {
    const tradeIndices = Object.keys(trades.entry_date);

    return tradeIndices.map((id) => ({
        entry_date: trades.entry_date[id],
        exit_date: trades.exit_date[id],
        entry_price: trades.entry_price[id],
        exit_price: trades.exit_price[id],
        return: trades.return[id],
        duration: trades.duration[id],
    }));
}

function validatePeriod(period: string): boolean {
    if (period === "") {
        return false;
    }

    /* Validates period format supported by yfinance Ticker.history function */
    const periodPattern = /^(\d+[dmy]|\d+mo|ytd|max)$/i;

    return periodPattern.test(period.trim());
}

export function validateInput(strategies: StrategyConfig[], ticker: string, initialCapital: number, period: string): { success: boolean, error: string } {
    if (strategies.length === 0) {
        return { success: false, error: "No strategies provided" }
    }

    if (ticker === "") {
        return { success: false, error: "Ticker is required" }
    }

    if (initialCapital <= 0) {
        return { success: false, error: "Initial capital must be greater than 0" }
    }

    if (period === "") {
        return { success: false, error: "Period is required" }
    }

    if (!validatePeriod(period)) {
        return { success: false, error: "Invalid period format. Supported periods: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max" }
    }

    return { success: true, error: "" };
}



