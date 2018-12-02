#notes
#cant use multprocessing bc of pickle

import requests
import time
import json
import datetime
import pandas as pd
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import SignatureTranslatedAnonymousPackage
import cpdb

class coin:
    def __init__(self, CoinName):
        self.coinName = CoinName
    
    def get_coin_price(self):
        coin = self.coinName
        if coin == 'xrp':
            coin ='ripple'
        api_request = requests.get("https://api.coinmarketcap.com/v1/ticker"+ coin)
        api_json = json.loads(api_request.text)
        price = [api_json[0]['price_usd']]
        return price
    
    def feature_maker(self, price_holder):
        price_holder = []
        while len(price_holder) < 100:
            time.sleep(18)
            price_holder.append(coin.get_coin_price())
        stats = coin.get_arima_rsi(price_holder)
        high = max(price_holder)
        low = min(price_holder)
        now = datetime.datetime.now()
        price = coin.get_coin_price()
        cpdb.insert_utility(self.coinName, now, price, stats[0], stats[1], high, low)
    
        
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
    
    def feature_maker_train(self, price_holder):
        stats = coin.get_arima_rsi(price_holder)
        high = max(price_holder)
        low = min(price_holder)
        price = price_holder[0]
        return [price, stats[0], stats[1], high, low]