import pandas as pd
import numpy as np
from datetime import datetime
import pandas_datareader.data as web
import matplotlib.pyplot as plt
from matplotlib import style
import backtrader.indicators as bti
import stock_indicators as sti
import constants
import date_util

"""
Class for receiving data from yahoo finance
Should not be runnable from terminal, only from olga.py
"""

start_time = datetime(2000, 01, 01)
end_time = datetime.now().date()
result_days = constants.RESULT_DAYS


def get_stock_data(stock_symbol):

    print("Downloading " + stock_symbol + ' data...'),

    # Receive stock info
    split_df = get_stock_actions(stock_symbol)

    df = web.DataReader(stock_symbol, 'yahoo', start_time, end_time)
    print("DONE!")

    if not split_df.empty:
        df = correct_prices(df, split_df)
    else:
        print("No splits was found.")

    print("Calculating indicators..."),
    df['Day of week'] = date_util.get_weekday_from_serie(df.index)
    df['Month'] = date_util.get_month_from_serie(df.index)

    # Remove days when OMXS is closed ('Volume == 0')
    df = df[df.Volume != 0]
    # df = df.drop('High', 1).drop('Low', 1).drop('Open', 1).drop('Close', 1)
    df = df.drop('Open', 1).drop('Adj Close', 1)

    prices = df['Close']

    df['Price Delta% 1'] = sti.delta_percent(prices, 1)
    df['Price Delta% 2'] = sti.delta_percent(prices, 2)
    df['Price Delta% 3'] = sti.delta_percent(prices, 3)
    # df['Price Delta% 7'] = sti.delta_percent(prices, 7)
    # df['Price Delta% 30'] = sti.delta_percent(prices, 30)

    df['Volume Delta 1'] = sti.delta_percent(df['Volume'], 1)
    df['Volume Delta 2'] = sti.delta_percent(df['Volume'], 2)
    df['Volume Delta 3'] = sti.delta_percent(df['Volume'], 3)
    # df['Volume Delta 7'] = sti.delta_percent(df['Volume'], 7)

    df['RSI 14'] = sti.rsi(prices)
    df['RSI Delta 1'] = sti.delta(df['RSI 14'], 1)
    df['RSI Delta 2'] = sti.delta(df['RSI 14'], 2)
    df['RSI Delta 3'] = sti.delta(df['RSI 14'], 3)
    # df['RSI Delta 7'] = sti.delta(df['RSI 14'], 7)

    df['SMA 15'] = sti.sma(prices, 15)
    df['SMA 50'] = sti.sma(prices, 50)
    df['SMA Diff'] = sti.diff(df['SMA 15'], df['SMA 50'])
    df['SMA Diff Delta 1'] = sti.delta(df['SMA Diff'], 1)
    df['SMA Diff Delta 2'] = sti.delta(df['SMA Diff'], 2)
    df['SMA Diff Delta 3'] = sti.delta(df['SMA Diff'], 3)
    # df['SMA Diff Delta 7'] = sti.delta(df['SMA Diff'], 7)

    df['SMA 10'] = sti.sma(prices, 10)
    df['EMA 10'] = sti.ema(prices, 10)
    df['EMA Diff'] = sti.diff(df['SMA 10'], df['EMA 10'])
    df['EMA Diff Delta 1'] = sti.delta(df['EMA Diff'], 1)
    df['EMA Diff Delta 2'] = sti.delta(df['EMA Diff'], 2)
    df['EMA Diff Delta 3'] = sti.delta(df['EMA Diff'], 3)
    # df['EMA-Diff-Delta-7'] = sti.delta(df['EMA-Diff'], 7)

    df['MACD'] = sti.macd(prices)
    df['MACD signal'] = sti.macd_signal(df['MACD'])
    df['MACD Diff'] = sti.diff(df['MACD'], df['MACD signal'])
    df['MACD Diff Delta 1'] = sti.delta(df['MACD Diff'], 1)
    df['MACD Diff Delta 2'] = sti.delta(df['MACD Diff'], 2)
    df['MACD Diff Delta 3'] = sti.delta(df['MACD Diff'], 3)
    # df['MACD Diff Delta 7'] = sti.delta(df['MACD Diff'], 7)

    df['Stochastic K'], df['Stochastic D'] = sti.stochastic(df['High'], df['Low'], prices)
    df['Stochastic Diff'] = sti.diff(df['Stochastic K'], df['Stochastic D'])
    df['Stochastic K Delta 1'] = sti.delta(df['Stochastic K'], 1)
    df['Stochastic K Delta 2'] = sti.delta(df['Stochastic K'], 2)
    df['Stochastic K Delta 3'] = sti.delta(df['Stochastic K'], 3)
    # df['Stochastic K Delta 7'] = sti.delta(df['Stochastic K'], 7)
    df['Stochastic D Delta 1'] = sti.delta(df['Stochastic D'], 1)
    df['Stochastic D Delta 2'] = sti.delta(df['Stochastic D'], 2)
    df['Stochastic D Delta 3'] = sti.delta(df['Stochastic D'], 3)
    # df['Stochastic D Delta 7'] = sti.delta(df['Stochastic D'], 7)
    df['Stochastic Diff Delta 1'] = sti.delta(df['Stochastic Diff'], 1)
    df['Stochastic Diff Delta 2'] = sti.delta(df['Stochastic Diff'], 2)
    df['Stochastic Diff Delta 3'] = sti.delta(df['Stochastic Diff'], 3)
    # df['Stochastic Diff Delta 7'] = sti.delta(df['Stochastic Diff'], 7)

    df['Aroon Positive'], df['Aroon Negative'] = sti.aroon(df['High'].values, df['Low'].values)
    df['ADX'] = sti.adx(df['High'].values, df['Low'].values, prices.values)
    df['ADX Delta 1'] = sti.delta(df['ADX'], 1)
    df['ADX Delta 2'] = sti.delta(df['ADX'], 2)
    df['ADX Delta 3'] = sti.delta(df['ADX'], 3)
    # df['ADX Delta 7'] = sti.delta(df['ADX'], 7)

    df['CCI 20'] = sti.cci(df['High'].values, df['Low'].values, prices.values)
    df['CCI 20 Delta 1'] = sti.delta(df['CCI 20'], 1)
    df['CCI 20 Delta 2'] = sti.delta(df['CCI 20'], 2)
    df['CCI 20 Delta 3'] = sti.delta(df['CCI 20'], 3)
    # df['CCI 20 Delta 7'] = sti.delta(df['CCI 20'], 7)

    df['MOM'] = sti.mom(prices.values)
    df['MOM Delta 1'] = sti.delta(df['MOM'], 1)
    df['MOM Delta 2'] = sti.delta(df['MOM'], 2)
    df['MOM Delta 3'] = sti.delta(df['MOM'], 3)
    # df['MOM Delta 7'] = sti.delta(df['MOM'], 7)

    df = df.drop('High', 1).drop('Low', 1)
    last_day_data = df.tail(1)

    df['Rating ' + str(result_days) + ' Days'] = sti.get_rating_from_result(sti.result_percent(prices, result_days))

    df = df[df['SMA 50'] != 0]
    df = df[:-result_days]

    print("DONE!")
    print(last_day_data)
    return df, last_day_data


def get_stock_actions(stock_symbol):
    df = web.DataReader(stock_symbol, 'yahoo-actions', start_time, end_time)
    df = df[df['action'] != 'DIVIDEND']
    return df


def correct_prices(stock_data, split_data):
    print('Found ' + str(len(split_data.index)) + ' splits:')
    for split_date, split in split_data.iterrows():
        print(' - Split ' + str(split_date) + ', value: ' + str(split['value']))
    print('Correcting data based on the splits...'),
    for stock_date, stock in stock_data.iterrows():
        for split_date, split in split_data.iterrows():
            if stock_date < split_date:
                # Multiply with split['value']
                stock_data.set_value(stock_date, 'Close', stock['Close'] * split['value'])
                stock['Close'] = stock['Close'] * split['value']
                stock_data.set_value(stock_date, 'High', stock['High'] * split['value'])
                stock['High'] = stock['High'] * split['value']
                stock_data.set_value(stock_date, 'Low', stock['Low'] * split['value'])
                stock['Low'] = stock['Low'] * split['value']
    print('DONE!')
    return stock_data
