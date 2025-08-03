import { type Trade } from "../utils/types";

export default function TradeTable({ trades }: { trades: Trade[] }) {
    return (
        <div className="bg-white rounded-lg shadow-lg border border-gray-100 overflow-hidden">
              <table className="w-full table-auto">
                <thead className="bg-gray-50 border-b border-gray-200">
                  <tr>
                    <th className="px-3 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                      Entry Date
                    </th>
                    <th className="px-3 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                      Exit Date
                    </th>
                    <th className="px-3 py-4 text-right text-xs font-semibold text-gray-600 uppercase tracking-wider">
                      Entry Price
                    </th>
                    <th className="px-3 py-4 text-right text-xs font-semibold text-gray-600 uppercase tracking-wider">
                      Exit Price
                    </th>
                    <th className="px-3 py-4 text-right text-xs font-semibold text-gray-600 uppercase tracking-wider">
                      Return
                    </th>
                    <th className="px-3 py-4 text-center text-xs font-semibold text-gray-600 uppercase tracking-wider">
                      Duration
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-100">
                  {trades.map((trade: Trade, index: number) => (
                    <tr key={trade.entry_date + index} className="hover:bg-gray-50 transition-colors duration-150">
                      <td className="px-3 py-4 text-sm text-gray-900 font-medium whitespace-nowrap">
                        {new Date(trade.entry_date).toLocaleDateString()}
                      </td>
                      <td className="px-3 py-4 text-sm text-gray-900 font-medium whitespace-nowrap">
                        {new Date(trade.exit_date).toLocaleDateString()}
                      </td>
                      <td className="px-3 py-4 text-sm text-gray-900 text-right font-mono whitespace-nowrap">
                        ${Number(trade.entry_price).toFixed(2)}
                      </td>
                      <td className="px-3 py-4 text-sm text-gray-900 text-right font-mono whitespace-nowrap">
                        ${Number(trade.exit_price).toFixed(2)}
                      </td>
                      <td className={`px-3 py-4 text-sm text-right font-mono font-semibold whitespace-nowrap ${
                        Number(trade.return) >= 0 ? 'text-green-600' : 'text-red-600'
                      }`}>
                        {Number(trade.return) >= 0 ? '+' : ''}{(Number(trade.return) * 100).toFixed(2)}%
                      </td>
                      <td className="px-3 py-4 text-sm text-gray-600 text-center whitespace-nowrap">
                        {trade.duration} days
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
    )       
}