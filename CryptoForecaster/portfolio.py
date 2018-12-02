import coin

'''Encapsulates the portfolio class and its related actions, 
    lergely self-explanatory in function'''
    
class portfolio:
        def __init__(self):
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

        ''' This isn't used in the code ready, but can be called in the driver function
            to get values - profit will be represented using matplotlib as a 
            time-series over time '''
            
        def get_portfolio_value(self):
            print( self.valuation + float(coin.get_coin_price()) * self.coinPurse)

                
                
        
        

