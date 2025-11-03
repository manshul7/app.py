# 📈 Portfolio Optimization & Efficient Frontier Visualizer

This is an interactive web application built with Streamlit that performs portfolio optimization based on Modern Portfolio Theory (MPT).

It fetches live stock data, runs a Monte Carlo simulation to generate thousands of possible portfolio weightings, and plots the **Efficient Frontier**. The app helps users visualize the trade-off between risk and return and identifies the optimal portfolios for:
* **Maximum Sharpe Ratio** (the best risk-adjusted return)
* **Minimum Volatility** (the safest portfolio)



---

## 🚀 Live Application

You can access the live application here:
https://j2okvvgss7jyelipngtnts.streamlit.app/

---

## ✨ Features

* **Interactive Data:** Fetches live historical stock data using the `yfinance` library.
* **Monte Carlo Simulation:** Runs thousands of simulations to model different portfolio asset allocations.
* **Efficient Frontier Plot:** An interactive scatter plot visualizing all simulated portfolios based on their risk (volatility) and return.
* **Color-Coded Risk:** Portfolios are color-coded by their Sharpe Ratio, making it easy to spot the most efficient ones (higher is better).
* **Optimal Portfolios:** Automatically finds and highlights:
    * The **Maximum Sharpe Ratio Portfolio** (marked with a large red star).
    * The **Minimum Volatility Portfolio** (marked with a large blue circle).
* **Detailed Weights:** Displays the exact asset allocation (weights) in a clean percentage format for the best-performing portfolio.

---

## 🛠️ Tech Stack

This project is built using the following libraries:

* **Streamlit:** For building and serving the interactive web app.
* **Pandas:** For data manipulation and analysis.
* **NumPy:** For high-performance numerical calculations and matrix operations ($w^T \Sigma w$).
* **yfinance:** For downloading historical stock market data from Yahoo! Finance.
* **Matplotlib:** For creating the data visualizations and the Efficient Frontier plot.

---
