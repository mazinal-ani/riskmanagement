from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from scipy.stats import norm
import yfinance as yf
#import pandas as pd
import numpy as np

app = Flask(__name__)
CORS(app)

# VaR API Route
@app.route('/valueatrisk', methods=['POST'])
def valueatrisk():
        
    data = request.get_json()
    print(data)
    stocks = data['stockData'].split()
    weights = data['weightData'].split()
    weights = [eval(stock) for stock in weights]
    size = len(stocks)
    

    def daily_return(historical_df):

        daily_returns = [None]

        for i in range(historical_df.shape[0] - 1):

            day_close = historical_df.loc[historical_df.index[i], 'Close']
            next_close = historical_df.loc[historical_df.index[i+1], 'Close']
            percent_change = ((next_close / day_close) - 1) * 100
            daily_returns.append(percent_change)

            return daily_returns


    def asset_variance(historical_df, mean):

        variance = 0

        for i in range(historical_df.shape[0]):
            variance += (mean - historical_df.loc[historical_df.index[i], 'Percent Change']) ** 2
        
        variance /= historical_df.shape[0] - 1

        return variance


    def find_covariances(list_of_returns):

        covariances = np.cov(list_of_returns, ddof=1)
        return covariances




    #******************************************************************************************************
    # Main
    #******************************************************************************************************


    total_daily_returns = []
    mean_returns = []
    variances = []


    def calculate_var(n, confidence_level, portfolio, weights):

        for stock_symbol in portfolio:

            ticker = yf.Ticker(stock_symbol)
            ticker_historical = ticker.history(period='1y', interval='1d')

            daily_change_arr = daily_return(ticker_historical)
            total_daily_returns.append(daily_change_arr)

            ticker_historical['Percent Change'] = daily_change_arr
            ticker_historical.drop(index=0, inplace=True)

            start = ticker_historical.loc[ticker_historical.index[0], 'Close']
            end = ticker_historical.loc[ticker_historical.index[-1], 'Close']

            mean_return = (((end / start) - 1) * 100) / ticker_historical.shape[0]

            variance = asset_variance(ticker_historical, mean_return)

            mean_returns.append(mean_return)
            variances.append(variance)

        covariances = find_covariances(total_daily_returns)



        #Calculate Portfolio Variance and Standard Deviation

        n = len(mean_returns)

        portfolio_variance = sum(weights[i] * weights[j] * covariances[i][j] for i in range(n) for j in range(n))

        portfolio_std = portfolio_variance ** 0.5



        z_score = norm.ppf(confidence_level)

        value_at_risk = portfolio_std * z_score

        return (value_at_risk)

    return jsonify({'Value at Risk': calculate_var(size, 0.95, stocks, weights)})




if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)


