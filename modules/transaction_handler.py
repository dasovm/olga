import os
import export_data as ed
import import_data as id
import constants as pc
import pandas as pd


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

    try:
        price = float("%.3f" % last_day_data.loc[date]['Close'])
        is_bought = get_if_is_bought(df, prediction)
        signal = get_prediction_text(prediction, is_bought)
        since_buy = get_percent_since_buy(df,
            get_prediction_text(prediction, is_bought),
            is_bought,
            last_day_data['Close'][0])
        df.loc[date] = [price, signal, is_bought, since_buy]
        ed.export_to_csv(df, ticker, path)
    except Exception, e:
        print e


def get_if_is_bought(df, prediction):
    try:
        if len(df.index) < 1:
            return False
        else:
            yester_df = df.tail(1)
            if (yester_df['Signal'].any() == 'BUY'):
                return True
            else:
                return bool(yester_df['Is Bought'].any())
    except Exception, e:
        print e
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
        buy_price = buy_df['Price'][0]
        return ((last_price - buy_price) / buy_price) * 100
    else:
        return 0
