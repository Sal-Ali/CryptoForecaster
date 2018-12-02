import sqlite3


''' This file encapsulates the forecaster's database management system'''
''' Naturally, table creation was done prior and this is mostly for show'''

db = 'cryptoforecaster.db'

''' data base connection manager '''
def create_connection(file):
    try:
        conn = sqlite3.connect(file, timeout=10)
        return conn
    except sqlite3.Error as e:
        print(e)
    return None

''' table creation utility '''
def create_table_utility(conn, table):
    try:
        c = conn.cursor()
        c.execute(table)
    except sqlite3.Error as e:
        print(e)

''' function to call for new table creation '''
def create_table(query):
    conn = create_connection(db)
    if conn is not None:
        for table in query:
            create_table_utility(conn, table)
    else:
        print('database error')
    conn.close()
    
''' inserts into selected coin, to avoid sql injection '''
''' (good practice I guess even though db is local) query is repeated'''
''' instead of manipulated by string ''' 
def insert_utility(coin, date, price, arima, rsi, high, low, recommendation):
    conn = create_connection(db)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
    c = conn.cursor()
    if coin == 'btc':
        c.execute('''INSERT INTO btc(date, price, arima, rsi, high, low, recommendation)
        VALUES(:date, :price, :arima, :rsi, :high, :low, :recommendation)''',
        {'date':date, 'price':price, 'arima':arima, 'rsi':rsi,
         'high':high,'low':low, 'recommendation':recommendation})
    if coin == 'eth':
        c.execute('''INSERT INTO eth(date, price, arima, rsi, high, low, recommendation)
        VALUES(:date, :price, :arima, :rsi, :high, :low, :recommendation)''',
        {'date':date, 'price':price, 'arima':arima, 'rsi':rsi,
         'high':high,'low':low, 'recommendation':recommendation})
    if coin == 'tron':
        c.execute('''INSERT INTO tron(date, price, arima, rsi, high, low)
        VALUES(:date, :price, :arima, :rsi, :high, :low)''',
        {'date':date, 'price':price, 'arima':arima, 'rsi':rsi,
         'high':high,'low':low})
    if coin == 'iota':
        c.execute('''INSERT INTO iota(date, price, arima, rsi, high, low)
        VALUES(:date, :price, :arima, :rsi, :high, :low)''',
        {'date':date, 'price':price, 'arima':arima, 'rsi':rsi,
         'high':high,'low':low})
    if coin == 'xrp':
        c.execute('''INSERT INTO xrp(date, price, arima, rsi, high, low)
        VALUES(:date, :price, :arima, :rsi, :high, :low)''',
        {'date':date, 'price':price, 'arima':arima, 'rsi':rsi,
         'high':high,'low':low})
    conn.commit()
    conn.close()
    
def retrieve(coin):
    conn = create_connection(db)
    c = conn.cursor()
    if coin == 'btc':
        c.execute('''SELECT * from btc''')
    if coin == 'eth':
        c.execute('''SELECT * from eth''')
    conn.commit()
    result = c.fetchall()
    conn.close()
    return result 



