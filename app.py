import numpy as np 
import pandas as pd 
import math 
import yfinance as yf 
import matplotlib.pyplot as plt
import streamlit as st



st.title("📈 Portfolio Optimization Engine")
st.write("This app runs a Monte Carlo simulation to find the optimal portfolios based on the Efficient Frontier.")


st.sidebar.header("User Inputs")


user_input = st.sidebar.text_input("Enter stock tickers (space-separated)", "AAPL MSFT GOOG AMZN")
start_date = st.sidebar.date_input("Start date", pd.to_datetime('2020-01-01'))
end_date = st.sidebar.date_input("End date", pd.to_datetime('today'))
num_simulations = st.sidebar.slider("Number of Simulations", 1000, 50000, 20000, 1000)
risk_free = st.sidebar.slider("Risk-Free Rate (%)", 0.0, 5.0, 2.0, 0.1) / 100


if st.sidebar.button("Run Optimization"):

    
    
    tickers = user_input.split()
    st.write(f"### Portfolio: {', '.join(tickers)}")

   
    with st.spinner(f"Downloading data for {tickers}..."):
        data = yf.download(tickers, start=start_date, end=end_date)
    
    if data.empty:
        st.error("Could not download data. Check tickers and date range.")
    else:
        st.subheader("Historical Data")
        st.dataframe(data['Close'].tail()) 

       
        returns = data['Close'].pct_change().dropna()
        
        
        ann_return = returns.mean() * 252
        cov_return = returns.cov() * 252

        num_assets = len(tickers)
        result = []
        
        
        st.subheader("Running Monte Carlo Simulation...")
        progress_bar = st.progress(0)

        for i in range(num_simulations):
          
            weight = np.random.random(num_assets)
            weight /= np.sum(weight)
            
           
            portfolio_return = np.dot(weight, ann_return)
            port_variance = weight.T @ cov_return @ weight
            port_risk = np.sqrt(port_variance)
            sharpe = (portfolio_return - risk_free) / port_risk
            
            result.append({
                'return': portfolio_return,
                'risk': port_risk,
                'sharpe': sharpe,
                'weights': weight
            })
            
            
            if (i+1) % (num_simulations // 100) == 0:
                progress_bar.progress((i+1) / num_simulations)
        
        progress_bar.empty() 
        result_df = pd.DataFrame(result)

        

        
        max_sharpe = result_df.loc[result_df['sharpe'].idxmax()]
        min_vol = result_df.loc[result_df['risk'].idxmin()]

        
        st.subheader("Optimal Portfolios")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Max Sharpe Ratio Portfolio")
            st.write(f"**Annual Return:** {max_sharpe['return']:.2%}")
            st.write(f"**Annual Risk:** {max_sharpe['risk']:.2%}")
            st.write(f"**Sharpe Ratio:** {max_sharpe['sharpe']:.2f}")
            st.write("**Weights:**")
            st.dataframe(pd.Series(max_sharpe['weights'], index=tickers, name="Weight").map(lambda x: f"{x:.2%}"))

        with col2:
            st.markdown("#### Minimum Volatility Portfolio")
            st.write(f"**Annual Return:** {min_vol['return']:.2%}")
            st.write(f"**Annual Risk:** {min_vol['risk']:.2%}")
            st.write(f"**Sharpe Ratio:** {min_vol['sharpe']:.2f}")
            st.write("**Weights:**")
            st.dataframe(pd.Series(min_vol['weights'], index=tickers, name="Weight").map(lambda x: f"{x:.2%}"))
            
       
        
        st.subheader("Efficient Frontier")
        
        
        fig, ax = plt.subplots(figsize=(12, 7))
        
        
        ax.scatter(
            result_df['risk'], 
            result_df['return'], 
            c=result_df['sharpe'], 
            cmap='viridis', 
            marker='o',
            s=10, 
            alpha=0.3
        )
        
        
        ax.scatter(
            max_sharpe['risk'],
            max_sharpe['return'], 
            marker='*', 
            color='r', 
            s=500, 
            label='Max Sharpe Ratio'
        )
        ax.scatter(
            min_vol['risk'], 
            min_vol['return'], 
            marker='o',
            edgecolors='b', 
            facecolors='none', 
            s=500, 
            label='Minimum Volatility'
        )
        
        ax.set_title('Portfolio Optimization - Efficient Frontier')
        ax.set_xlabel('Annualized Risk (Volatility)')
        ax.set_ylabel('Annualized Return')
        ax.legend()
        
        
        st.pyplot(fig)