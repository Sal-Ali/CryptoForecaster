import coin

class portfolio:
        def __init__(self, CoinName):
            self.coinName = CoinName
            self.valuation = float(100,000)
            self.coinPurse = float(0)
        
        def buy(self):
            if self.valuation == 0:
                return
            price = coin.get_coin_price()
            if self.valuation < price:
                proportion = float(self.valuation) / price
                self.valuation = 0
                self.coinPurse += proportion
            else:
                self.valuation -= price
                self.coinPurse += 1
                
        def sell(self):
            if self.coinPurse == 0:
                return
            price = coin.get_coin_price()
            if self.coinPurse < 1:
                proportion = float(self.coinPurse) * price
                self.valuation += proportion
                self.coinPurse = 0
            else:
                self.valuation += price
                self.coinPurse -= 1
        
        def get_portfolio_value(self):
            return self.valuation + coin.get_coin_price() * self.coinPurse
        ''' track portfolio value over time in main class, then plt '''
        ''' create algorithmic now '''
                
                
        
        

