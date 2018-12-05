''' Short note: 
    
    I am aware that the standard is to use Jupyter Notebook,
    my personal preference is in Spyder and for purposes of 
    convenience this was what I chose, as a result code is frequently
    commented in and out. On Github, I will leave all code uncommented
    as this portion of code has zero bearing to my actual program besides
    serving as record of exactly how I created my initial model'''
import pandas as pd
from pathlib import Path
from coin import coin
import pickle

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import Imputer
from xgboost import XGBClassifier
from sklearn.metrics import zero_one_loss
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV

''' Initial data gathered from gemini (free) '''
c = coin('train')
btc_file_path = Path("D:/btc.csv")
eth_file_path = Path("D:/eth.csv")

btc_dat = pd.read_csv(btc_file_path)
eth_dat = pd.read_csv(eth_file_path)

btc_dat = btc_dat.head(100000)
eth_dat = eth_dat.head(100000)

btc_prices = btc_dat.Open
eth_prices = eth_dat.Open


btc_features = []
eth_features = []
btc_labels = []
eth_labels = []

 # price, arima, rsi, high, low | label
def features(prices, dataset, labels, features):
    count = 0
    while count != 99900:
        prices_h = []
        for i in range(100):
            prices_h.append(prices[count+ i])
            count += 1
        stats = c.feature_maker_train(prices_h)
        features.append(stats)
        if dataset.Close[count] <= stats[0]:
            labels.append(1) # buy
        else:
            labels.append(2) # sell
        
features(btc_prices, btc_dat, btc_labels, btc_features)
features(eth_prices, eth_dat, eth_labels, eth_features)

label_1 = pickle.dumps(btc_labels)
label_2 = pickle.dumps(eth_labels)


btc_f = pd.DataFrame(btc_features, columns=['price','arima','rsi','high','low'])
eth_f = pd.DataFrame(eth_features, columns=['price','arima','rsi','high','low'])

btc_features = pickle.dumps(btc_f)
eth_features = pickle.dumps(eth_f)
''' pickle split here to reduce repetitiveness ''' 

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 
# Had to do it for cross-validation


btc_f = pickle.loads(btc_features)
eth_f = pickle.loads(eth_features)
btc_labels = pickle.loads(label_1)
eth_labels = pickle.loads(label_2)

btc_l = pd.Series(btc_labels)
eth_l = pd.Series(btc_labels)

btc_y = btc_l
btc_X = btc_f
train_X, test_X, train_y, test_y = train_test_split(btc_X.as_matrix(), btc_y.as_matrix(), test_size=0.01)

eth_y = eth_l
eth_X = eth_f
train_X1, test_X1, train_y1, test_y1 = train_test_split(eth_X.as_matrix(), eth_y.as_matrix(), test_size=0.01)
''' first attempt at model training '''
btc_model = XGBClassifier(silent=True)
btc_model.fit(train_X, train_y, verbose=False)
btc_pred = btc_model.predict(test_X)

eth_model = XGBClassifier(silent=True)
eth_model.fit(train_X1, train_y1, verbose=False)
eth_pred = eth_model.predict(test_X1)

print(" btc  Error : " + str(zero_one_loss(btc_pred, test_y)))
print(" eth Error : " + str(zero_one_loss(eth_pred, test_y1)))

''' initial accuracy is 68% and 55% ... not the best, my attempt at tuning '''

btc_pipeline = Pipeline([('imputer', Imputer()), ('xgb_c', XGBClassifier())])
eth_pipeline = Pipeline([('imputer', Imputer()), ('xgb_c', XGBClassifier())])

param_grid = {
    "xgb_c__n_estimators": [1, 10, 50, 100, 500, 1000],
    "xgb_c__learning_rate": [0.01, 0.1, 0.5, 1, 10],
    "xgb_c__early_stopping_rounds": [3, 6, 10, 12],
}

''' Yes, this took very long but I had time and was curious '''

fit_params_btc = {"xgb_c__eval_set": [(test_X, test_y)], 
              "xgb_c__eval_metric": 'error', 
              "xgb_c__verbose": False}

fit_params_eth = {"xgb_c__eval_set": [(test_X1, test_y1)], 
              "xgb_c__eval_metric": 'error', 
              "xgb_c__verbose": False}

searchCV_btc = GridSearchCV(btc_pipeline, cv=5,
                            param_grid=param_grid, fit_params=fit_params_btc)

searchCV_eth = GridSearchCV(eth_pipeline, cv=5,
                        param_grid=param_grid, fit_params=fit_params_eth)

searchCV_btc.fit(train_X, train_y)  
searchCV_eth.fit(train_X1, train_y1)  

print(searchCV_btc.best_params_)
print(searchCV_eth.best_params_)

'''
Results,
{'xgb_c__early_stopping_rounds': 3, 'xgb_c__learning_rate': 0.1, 'xgb_c__n_estimators': 500}
{'xgb_c__early_stopping_rounds': 3, 'xgb_c__learning_rate': 1, 'xgb_c__n_estimators': 500}'''

''' Trying a little more here '''

param_grid_2 = {
    "xgb_c__n_estimators": [500, 750],
    "xgb_c__learning_rate": [0.05, 0.1, 0.2, 1, 1.5, 2],
    "xgb_c__early_stopping_rounds": [2, 3 ,4],
}

searchCV_btc = GridSearchCV(btc_pipeline, cv=5,
                            param_grid=param_grid_2, fit_params=fit_params_btc)

searchCV_eth = GridSearchCV(eth_pipeline, cv=5,
                        param_grid=param_grid_2, fit_params=fit_params_eth)

searchCV_btc.fit(train_X, train_y)  
searchCV_eth.fit(train_X1, train_y1)  

print(searchCV_btc.best_params_)
print(searchCV_eth.best_params_)

''' Little surprised here... 
{'xgb_c__early_stopping_rounds': 2, 'xgb_c__learning_rate': 0.05, 'xgb_c__n_estimators': 750}
{'xgb_c__early_stopping_rounds': 2, 'xgb_c__learning_rate': 0.05, 'xgb_c__n_estimators': 500}
Let's try it  '''

btc_model = XGBClassifier(silent=True, learning_rate=0.05, early_stopping_rounds=2,
                          n_estiamtors=750)
btc_model.fit(train_X, train_y, verbose=False)
btc_pred = btc_model.predict(test_X)

eth_model = XGBClassifier(silent=True, learning_rate=0.05, early_stopping_rounds=2,
                          n_estimators=500)
eth_model.fit(train_X1, train_y1, verbose=False)
eth_pred = eth_model.predict(test_X1)

print(" btc  Error : " + str(zero_one_loss(btc_pred, test_y)))
print(" eth Error : " + str(zero_one_loss(eth_pred, test_y1)))

''' Surprisingly, more normalized error. Marginal decrease in btc error, but this is
    likely due to the fact that I actually cross validated this set.
    All in all 70% and 65% accurate - better than 50/50, I'll take it for now. '''

btc_model.save_model('btc_model.model')
eth_model.save_model('eth_model.model')
btc_model.save_model('btc_model.bin')
eth_model.save_model('eth_model.bin')
# Have to be safe, saved two copies
