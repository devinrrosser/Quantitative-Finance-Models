import yfinance as yf
import numpy as np

def run_lbo_screen(ticker_symbol, target_irr=0.20):
    print(f"\n--- Initializing LBO Screen for {ticker_symbol} ---")
    try:
        ticker = yf.Ticker(ticker_symbol)
        
        # 1. Fetch Trailing Financials
        financials = ticker.financials
        balance_sheet = ticker.balance_sheet
        
        ebitda = financials.loc['EBITDA'].iloc[0]
        total_debt = balance_sheet.loc['Total Debt'].iloc[0] if 'Total Debt' in balance_sheet.index else 0
        cash = balance_sheet.loc['Cash And Cash Equivalents'].iloc[0] if 'Cash And Cash Equivalents' in balance_sheet.index else 0
        
        # Current Market Enterprise Value
        market_cap = ticker.info.get('marketCap', 0)
        enterprise_value = market_cap + total_debt - cash
        entry_multiple = enterprise_value / ebitda
        
        # LBO Assumptions
        leverage_ratio = 0.60  # 60% Debt funding
        rev_growth = 0.05      # 5% annual EBITDA growth
        fcf_conversion = 0.50  # 50% of EBITDA goes to paying down debt
        interest_rate = 0.07   # 7% interest on debt
        
        # 2. Setup Transaction
        purchase_price = enterprise_value
        entry_debt = purchase_price * leverage_ratio
        sponsor_equity = purchase_price - entry_debt
        
        print(f"Entry Enterprise Value: ${purchase_price/1e9:.2f}Bn (Multiple: {entry_multiple:.1f}x)")
        print(f"Sponsor Equity Check:   ${sponsor_equity/1e9:.2f}Bn | Debt: ${entry_debt/1e9:.2f}Bn")
        
        # 3. 5-Year Projection Loop
        current_ebitda = ebitda
        current_debt = entry_debt
        
        for year in range(1, 6):
            current_ebitda *= (1 + rev_growth)
            interest_expense = current_debt * interest_rate
            free_cash_flow = (current_ebitda * fcf_conversion) - interest_expense
            
            # Pay down debt (cannot go below 0)
            current_debt = max(0, current_debt - free_cash_flow)
            
        # 4. Exit Valuation (Assuming multiple expansion/contraction matches entry)
        exit_ev = current_ebitda * entry_multiple
        exit_equity = exit_ev - current_debt
        
        # 5. Calculate Metrics
        moic = exit_equity / sponsor_equity
        irr = (moic ** (1/5)) - 1
        
        print(f"\nYear 5 Exit EV:         ${exit_ev/1e9:.2f}Bn")
        print(f"Remaining Debt:         ${current_debt/1e9:.2f}Bn")
        print(f"Ending Equity Value:    ${exit_equity/1e9:.2f}Bn")
        print(f"Projected MOIC:         {moic:.2f}x")
        print(f"Projected IRR:          {irr:.2%}")
        
        if irr >= target_irr:
            print(">>> STATUS: Strong Buyout Target (Passes Hurdle Rate) <<<")
        else:
            print(">>> STATUS: Fails Hurdle Rate <<<")
            
    except Exception as e:
        print(f"Screening failed for {ticker_symbol}: {e}")

# Run the screen
run_lbo_screen("URI")