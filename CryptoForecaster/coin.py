''' Main coin class, creates primary feature statistics, and maintains a portfolio object'''

import requests
import time
import json
import datetime
import pandas as pd
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import SignatureTranslatedAnonymousPackage
from decision_maker import get_recommendation
import cpdb
from portfolio import portfolio
import pickle

class coin:
    def __init__(self, CoinName):
        self.coinName = CoinName
        self.portfolio = portfolio()
        
    ''' Standard price retreiver using API'''
    def get_coin_price(self):
        coin = self.coinName
        if coin == 'xrp':
            coin ='ripple'
        api_request = requests.get("https://api.coinmarketcap.com/v1/ticker"+ coin)
        api_json = json.loads(api_request.text)
        price = [api_json[0]['price_usd']]
        return price
    
    '''Main function of the entire program/class updates model features, portfolio actions,
        sql inserts, and even backtesting'''
    def feature_maker(self):
        price_holder = []
        while len(price_holder) < 100:
            time.sleep(18)
            price_holder.append(coin.get_coin_price())
        stats = coin.get_arima_rsi(price_holder)
        high = max(price_holder)
        low = min(price_holder)
        now = datetime.datetime.now()
        price = coin.get_coin_price()
        features = [self.coinName, now, price, stats[0], stats[1], high, low]
        rec = get_recommendation(self.coinName, features)
        if rec == 1:
            self.portfolio.buy()
        elif rec == 2:
            self.portfolio.sell()
        cpdb.insert_utility(self.coinName, now, price, stats[0], stats[1],
                            high, rec)
        # necessary persistence with the portfolio for each coin
        portfolio = pickle.dumps(self.portfolio)
        self.portfolio = pickle.loads(portfolio)
    '''Calculates arima intercept using arima model on intermittent data, also
        gathers RSI.
        This is done through the use of the rpy2 interface significantly
        reducing code length for this portion'''  
    def get_arima_rsi(prices):
        df = pd.DataFrame(prices)
        pandas2ri.activate()
        calculate_models = """ calculate <- function(x, size=100){
                                x <- na.omit(x)
                                library(TTR)
                                library(stats)
                                x <- ts(x)
                                f <- function(m) class(try(solve(m),silent=T))=="matrix"
                                if(f(x)){
                                x[50] = x[50] + 2
                                }
                                arima <- arima(x, c(0,0,0))
                                rsi <- RSI(x, size-1)[size]
                                list <-c(arima$coef, rsi)
                                return(as.array(list))
                                }"""
        calculate = SignatureTranslatedAnonymousPackage(calculate_models, "calculate")
        stats = calculate.calculate(df, len(df))
        return stats
    '''Deprecated code, used primarily in the initial model training'''
    def feature_maker_train(self, price_holder):
        stats = coin.get_arima_rsi(price_holder)
        high = max(price_holder)
        low = min(price_holder)
        price = price_holder[0]
        return [price, stats[0], stats[1], high, low]