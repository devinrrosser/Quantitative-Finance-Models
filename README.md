Markdown
# Quantitative Finance & Operations Strategy Models

This repository contains a suite of Python-based quantitative models built to automate financial valuation, deal screening, and supply chain logistics. 

## 1. Automated LBO Fast-Screener (`lbo_screen.py`)
A dynamic leveraged buyout screening engine that interfaces with Yahoo Finance APIs to execute automated 5-year debt-paydown simulations. 
* **Business Use Case:** Accelerates Private Equity target origination by instantly calculating implied Internal Rate of Return (IRR) and Multiple on Invested Capital (MOIC) based on dynamic capital structure assumptions.

## 2. Logistics Network Optimization Engine (`supply_chain.py`)
A linear programming optimization model utilizing `scipy.optimize` to solve multi-node transportation constraints.
* **Business Use Case:** Minimizes aggregate distribution costs by routing products across simulated supply chain networks, mathematically balancing rigid factory supply caps against precise warehouse demand requirements.
* **Result Example:** Successfully routed 1,100 units across a 5-node domestic network to achieve an absolute minimum logistics cost floor of $3,200.

## 3. Macro-Reshoring Portfolio Screener (`etf_script.py`)
A theoretical factor-weighted portfolio model tracking macro-reshoring trends and domestic manufacturing leaders.
* **Business Use Case:** Replaces standard market-cap weighting with a dynamic Capital Expenditure (CapEx) factor screen, tilting allocations heavily toward industrial companies building physical infrastructure.

---
*Developed by Devin Rosser | University of Rochester*
