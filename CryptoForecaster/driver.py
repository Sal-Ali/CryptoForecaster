from coin import coin
import cpdb
import decision_maker as dm



''' Main driver class of the entire project, currently limited to the fact that 
    suitable data was only available for btc and eth, but will expand'''
    
''' Keep in note that this implementation requires Python 3.6.4+ and R 3.3 
    as well as required libraries in each language, I am working on a docker container
    to make this accessible on other machines when I can get high-degress of profit 
    on my own implementation.
    Currently, btc and eth remain profitable, despite current trends.
    '''
    
    
btc = coin('btc')
eth = coin('eth')
coins = ['btc','eth']
    
agenda = [btc, eth]
count = 0
n = 1000

''' Simple driver to perpetually run program and every n updates, retrain'''
while True:
    for c in agenda:
        c.feature_maker()
        count += 0.5
        if count % n == 0:
            c.portfolio.get_portfolio_value()
            for n in coins:
                dm.incremental_training(cpdb.retrieve(n))
                