print("--- SCRIPT INITIALIZED ---")

import yfinance as yf
from yfinance import EquityQuery

# 1. Build the "All-American" Screen
# This filters for US-based companies in the Industrials sector
q = EquityQuery('and', [
    EquityQuery('eq', ['region', 'us']),
    EquityQuery('eq', ['sector', 'Industrials'])
])

print("Scanning for the Top 20 US Reshoring Leaders...")

# 2. Execute the Screen
# We sort by market cap (descending) to get the "Blue Chip" leaders first
response = yf.screen(q, sortField='intradaymarketcap', sortAsc=False)
tickers = [quote['symbol'] for quote in response['quotes'][:20]]

portfolio_value = 10000
capex_results = {}

# 3. Pull CapEx Data
for ticker in tickers:
    try:
        stock = yf.Ticker(ticker)
        # Using TTM (Trailing Twelve Months) for the most current '26 data
        cf = stock.cashflow
        if 'Capital Expenditure' in cf.index:
            # Normalize to positive absolute value
            raw_capex = abs(cf.loc['Capital Expenditure'].iloc[0])
            capex_results[ticker] = raw_capex
    except Exception:
        continue

# 4. Sorting & Allocation Logic
sorted_capex = dict(sorted(capex_results.items(), key=lambda item: item[1], reverse=True))
total_capex = sum(sorted_capex.values())

print(f"\n{'Ticker':<10} | {'CapEx (Bn)':<12} | {'Weight %':<10} | {'Allocation ($)':<15}")
print("-" * 55)

for ticker, capex in sorted_capex.items():
    weight = capex / total_capex if total_capex > 0 else 0
    allocation = weight * portfolio_value
    print(f"{ticker:<10} | ${capex/1e9:>10.2f} | {weight:>9.2%} | ${allocation:>13.2f}")


    