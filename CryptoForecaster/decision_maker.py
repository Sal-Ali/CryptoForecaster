''' Contains all the model based code,
    provides recommendations for portfolio action, backtests, and incrementally trains
    the given XGBoost Classifier Model'''

from xgboost import XGBClassifier
import cpdb
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import Imputer
from sklearn.metrics import zero_one_loss
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV


btc_model = XGBClassifier()
eth_model = XGBClassifier()
btc_model = btc_model.load_model('btc_model.bin')
eth_model = eth_model.load_model('eth_model.bin')

model = {'btc':btc_model,'eth':eth_model,}
'''Delivers a recommendation based on model classification'''
def get_recommendation(coinName, features):
    coin_model = model.get(coinName)
    recommendation = coin_model.predict(features)
    
    return recommendation 

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

''' Initiates a back-test to determine model accuracy and fix incorrect values
for use in further model tuning'''
def backtest(dataset): #7 values
    mistakes = 0
    new_set = []
    for i in len(dataset - 1):
        row = dataset[i]
        next_row = dataset[i + 1]
        if (row[1] > next_row[1] and row[6] == 1) or (row[1] < next_row[1] and row[6] == 2):
            row[6] = 1 if row[6] == 2 else 2
            mistakes += 1
        new_set.append[row]
        if i + 1 == len(dataset):
            new_set.append[row]
    print('Error for this epoch: ' + (mistakes / float(len(dataset))) + 'improving model....')
    df = pd.DataFrame(new_set, columns=['date','price','arima','rsi','high','low','recommendation'])
    df.drop('date')
    return df
''' Backbone of the model update interface, takes the model and adapts it to new data,
    one big weakness of this program is the lack of further cross validation beyond the initial
    step, which is crucial for XGBoost'''
def incremental_training(coinName, dataset):
    coin_model = model.get(coinName)
    df = backtest(dataset)
    label = df.recommendation
    df.drop('recommendation')
    train_X, test_X, train_y, test_y = train_test_split(df.as_matrix(), label.as_matrix(), test_size=0.01)
    params_update({'process_type': 'update',
               'updater'     : 'refresh',
               'refresh_leaf': True})

    model_update = xgb.train(params_update, x_train, xgb_model=coin_model)
    coin_model.save_model(str(model.get(coinName)) + '.bin')

        