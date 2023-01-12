from flask import Flask, request, jsonify
from pandas_datareader import data as pdr
from flask_cors import CORS
from scipy.stats import norm
import yfinance as yf
import pandas as pd
import numpy as np
import datetime as dt

app = Flask(__name__)
CORS(app)


@app.route('/valueatrisk', methods=['POST'])
def valueatrisk():
        
    data = request.get_json()
    stocks = data['stockData'].split()
    confidence_level = eval(data['confidenceLevel']) / 100
    weights = data['weightData'].split()
    weights = np.array([eval(stock) for stock in weights])
    time_period = eval(data["timePeriod"])
    initial_investment = eval(data["initialInvestment"])


    stockdata = yf.download(stocks, start="2019-01-01", end=dt.date.today())['Adj Close']
    returns = stockdata.pct_change()
    returns.tail()
    mean_return_list = returns.mean()


    var_cov_matrix = returns.cov()

    portfolio_mean_returns = mean_return_list.dot(weights)
    portfolio_std = np.sqrt(weights.T.dot(var_cov_matrix).dot(weights))

    investment_mean_returns = (portfolio_mean_returns + 1) * initial_investment
    investment_std = initial_investment * portfolio_std

    portfolio_value_loss = norm.ppf(confidence_level, investment_mean_returns, investment_std)

    value_at_risk = initial_investment - portfolio_value_loss

    value_at_risk *= (time_period ** (1 / 2))

    if value_at_risk > 0:
        value_at_risk = 0
    else:
        value_at_risk *= -1
    
    value_at_risk = float(np.round(value_at_risk, 2))

    if value_at_risk > initial_investment: value_at_risk = initial_investment

    return jsonify(value_at_risk)




if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)


