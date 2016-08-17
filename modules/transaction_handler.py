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
        print 'Creating new stock_transaction file for ' + ticker
        index = pd.date_range(date, periods=1, freq='D')
        columns = ['Price', 'Signal', 'Is Bought', '% Since Buy']
        df = pd.DataFrame(index=index, columns=columns)

    try:
        print 'Calculatin info about ' + ticker
        price = float("%.3f" % last_day_data.loc[date]['Close'])
        print 'Price calculated:', price
        is_bought = get_if_is_bought(df, prediction)
        print 'Is bought calculated:', is_bought
        signal = get_prediction_text(prediction, is_bought)
        print 'Signal calculated:', signal
        since_buy = get_percent_since_buy(df,
            get_prediction_text(prediction, is_bought),
            is_bought,
            last_day_data['Close'][0])
        print 'Since buy calculated:', since_buy
        df.loc[date] = [price, signal, is_bought, since_buy]
        print 'Saved with index:', date
        ed.export_to_csv(df, ticker, path)
        if is_a_buy_or_sell(signal):
            print 'Signal is buy or sell:', signal
            if not os.path.exists(pc.TRANSACTION_LOG):
                print 'Trying to mkdir ', pc.TRANSACTION_LOG
                os.makedirs(pc.TRANSACTION_LOG)
            log_columns = ['Ticker', 'Signal', 'Price', '% Since Buy']
            if os.path.exists(pc.TRANSACTION_LOG + str(date) + '.csv'):
                print 'Trying to import logging data.'
                log_df = id.get_log_data_set_from_csv(date)
                print('Logging data is:', log_df)
            else:
                log_df = pd.DataFrame(columns=log_columns)
                print 'No logging data found. Creates new one.'
            # log_df.iloc[len(log_df.index) + 1] = [ticker, signal, price, since_buy]
            serie = pd.Series([ticker, signal, price, since_buy], index=log_columns)
            # serie = pd.Series({'Ticker': ticker, 'Signal': signal, 'Price': price, '% Since Buy': since_buy}, index=log_df.index)
            log_df = log_df.append(serie, ignore_index=True)
            print'New logging data is:', log_df
            ed.export_log_to_csv(log_df, date)
    except KeyError:
        raise KeyError(ticker + ' is not updated with data for ' + str(date))


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


def is_a_buy_or_sell(prediction):
    return prediction == 'BUY' or prediction == 'SELL'
