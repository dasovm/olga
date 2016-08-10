import os
import datetime
import export_data as ed
import import_data as id
import constants as pc
import pandas as pd
import numpy as np


def update_stock_transactions(ticker, prediction, date, last_day_data):
    path = pc.STOCK_TRANSACTIONS
    if not os.path.exists(path):
        os.makedirs(path)
    if os.path.exists(path + ticker + '.csv'):
        df = id.get_data_set_from_csv(ticker, path)
    else:
        index = pd.date_range(date, periods=1, freq='D')
        columns = ['Price', 'Signal', 'Is Bought', '% Since Buy']
        df = pd.DataFrame(index=index, columns=columns)
    df.loc[date]['Price'] = last_day_data.loc[date]['Close']
    is_bought = get_if_is_bought(df, prediction)
    df.loc[date]['Is Bought'] = is_bought
    df.loc[date]['Signal'] = get_prediction_text(prediction, is_bought)
    df.loc[date]['% Since Buy'] = get_percent_since_buy(df,
        get_prediction_text(prediction, is_bought),
        is_bought,
        last_day_data['Close'])
    ed.export_to_csv(df, ticker, path)


def get_if_is_bought(df, prediction):
    try:
        if len(df.index) <= 1:
            return False
        else:
            yester_df = df.tail(2).head(1)
            if (yester_df['Signal'] == 'BUY'):
                return True
            else:
                return yester_df['Is Bought'].bool()
    except Exception:
        return False


def get_prediction_text(prediction, is_bougth):
    if is_bougth:
        if prediction == 'SELL':
            return prediction
        else:
            return 'STAY LONG'
    else:
        if prediction == 'BUY':
            return prediction
        else:
            return 'STAY AWAY'


def get_percent_since_buy(df, prediction, is_bougth, last_price):
    if is_bougth or prediction == 'SELL':
        buy_df = df[df['Signal'] == 'BUY'].tail(1)
        buy_price = buy_df['Price']
        return (last_price - buy_price) * 100
    else:
        return 0