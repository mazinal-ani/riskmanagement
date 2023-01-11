from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import math
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
    #print(data)
    stocks = data['stockData'].split()
    confidence_level = eval(data['confidenceLevel']) / 100
    weights = data['weightData'].split()
    weights = [eval(stock) for stock in weights]
    size = len(stocks)
    #print (weights)
    #print(size)
    #print(stocks)
    

    def daily_return(historical_df):

        daily_returns = []

        for i in range(1, len(historical_df)):

            percent_change = (historical_df.iloc[i, 0] / historical_df.iloc[i - 1, 0]) - 1
            daily_returns.append(percent_change)

        return daily_returns


    def asset_variance(historical_df, mean):

        variance = 0

        for i in historical_df["Percent Change"]:
            variance += (mean - i) ** 2
        
        variance /= (len(historical_df) - 1)

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

            del ticker_historical['Open']
            del ticker_historical['High']
            del ticker_historical['Low']
            del ticker_historical['Volume']
            del ticker_historical['Dividends']
            del ticker_historical['Stock Splits']

            daily_change_arr = daily_return(ticker_historical)
            total_daily_returns.append(daily_change_arr)
            print(daily_change_arr)


            ticker_historical = ticker_historical.tail(-1)
            ticker_historical['Percent Change'] = daily_change_arr
            
            

            start = ticker_historical.iloc[0, 0]
            end = ticker_historical.iloc[-1, 0]

            mean_return = math.e ** (math.log(end/start) / len(ticker_historical))

            variance = asset_variance(ticker_historical, mean_return)

            mean_returns.append(mean_return)
            variances.append(variance)
            print("Hello")

        covariances = find_covariances(total_daily_returns)



        #Calculate Portfolio Variance and Standard Deviation

        n = len(mean_returns)

        portfolio_variance = sum(weights[i] * weights[j] * covariances[i][j] for i in range(n) for j in range(n))

        portfolio_std = portfolio_variance ** 0.5


        z_score = norm.ppf(confidence_level)

        value_at_risk = portfolio_std * z_score

        
        return (value_at_risk)

    return jsonify({'Value at Risk': calculate_var(size, confidence_level, stocks, weights)})
    #return jsonify("Hello")



if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)


