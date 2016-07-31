import pandas as pd
import numpy as np
from datetime import datetime
import pandas_datareader.data as web
import matplotlib.pyplot as plt
from matplotlib import style
import backtrader.indicators as bti
import stock_indicators as sti
import date_util

"""
Class for receiving data from yahoo finance
Should not be runnable from terminal, only from olga.py
"""

start_time = datetime(2000, 01, 01)
end_time = datetime.now().date()


def get_stock_data(stock_symbol):
	# Receive stock info
	df = web.DataReader(stock_symbol, 'yahoo', start_time, end_time)
	df['Date'] = df.index
	df['Day of week'] = date_util.get_weekday_from_serie(df['Date'])
	df['Month'] = date_util.get_month_from_serie(df['Date'])

	# Remove days when OMXS is closed ('Volume == 0')
	df = df[df.Volume != 0]
	# df = df.drop('High', 1).drop('Low', 1).drop('Open', 1).drop('Close', 1)
	df = df.drop('Open', 1).drop('Close', 1)

	prices = df['Adj Close']

	df['Price-Delta%-1'] = sti.delta_percent(prices, 1)
	df['Price-Delta%-3'] = sti.delta_percent(prices, 3)
	df['Price-Delta%-7'] = sti.delta_percent(prices, 7)
	df['Price-Delta%-30'] = sti.delta_percent(prices, 30)

	df['Volume-Delta-1'] = sti.delta_percent(df['Volume'], 1)
	df['Volume-Delta-3'] = sti.delta_percent(df['Volume'], 3)
	df['Volume-Delta-7'] = sti.delta_percent(df['Volume'], 7)

	df['RSI-14'] = sti.rsi(prices)
	df['RSI-Delta-1'] = sti.delta(df['RSI-14'], 1)
	df['RSI-Delta-3'] = sti.delta(df['RSI-14'], 3)
	df['RSI-Delta-7'] = sti.delta(df['RSI-14'], 7)

	df['SMA-15'] = sti.sma(prices, 15)
	df['SMA-50'] = sti.sma(prices, 50)
	df['SMA-Diff'] = sti.diff(df['SMA-15'], df['SMA-50'])
	df['SMA-Diff-Delta-1'] = sti.delta(df['SMA-Diff'], 1)
	df['SMA-Diff-Delta-3'] = sti.delta(df['SMA-Diff'], 3)
	df['SMA-Diff-Delta-7'] = sti.delta(df['SMA-Diff'], 7)

	df['SMA-10'] = sti.sma(prices, 10)
	df['EMA-10'] = sti.ema(prices, 10)
	df['EMA-Diff'] = sti.diff(df['SMA-10'], df['EMA-10'])
	df['EMA-Diff-Delta-1'] = sti.delta(df['EMA-Diff'], 1)
	df['EMA-Diff-Delta-3'] = sti.delta(df['EMA-Diff'], 3)
	df['EMA-Diff-Delta-7'] = sti.delta(df['EMA-Diff'], 7)

	df['MACD'] = sti.macd(prices)
	df['MACD-signal'] = sti.macd_signal(df['MACD'])
	df['MACD-Diff'] = sti.diff(df['MACD'], df['MACD-signal'])
	df['MACD-Diff-Delta-1'] = sti.delta(df['MACD-Diff'], 1)
	df['MACD-Diff-Delta-3'] = sti.delta(df['MACD-Diff'], 3)
	df['MACD-Diff-Delta-7'] = sti.delta(df['MACD-Diff'], 7)

	df['Stochastic-K'], df['Stochastic-D'] = sti.stochastic(df['High'], df['Low'], prices)
	df['Stochastic-Diff'] = sti.diff(df['Stochastic-K'], df['Stochastic-D'])
	df['Stochastic-K-Delta-1'] = sti.delta(df['Stochastic-K'], 1)
	df['Stochastic-K-Delta-3'] = sti.delta(df['Stochastic-K'], 3)
	df['Stochastic-K-Delta-7'] = sti.delta(df['Stochastic-K'], 7)
	df['Stochastic-D-Delta-1'] = sti.delta(df['Stochastic-D'], 1)
	df['Stochastic-D-Delta-3'] = sti.delta(df['Stochastic-D'], 3)
	df['Stochastic-D-Delta-7'] = sti.delta(df['Stochastic-D'], 7)
	df['Stochastic-Diff-Delta-1'] = sti.delta(df['Stochastic-Diff'], 1)
	df['Stochastic-Diff-Delta-3'] = sti.delta(df['Stochastic-Diff'], 3)
	df['Stochastic-Diff-Delta-7'] = sti.delta(df['Stochastic-Diff'], 7)

	df.drop('High', 1).drop('Low', 1)
	return df.tail(50)

	# Cut off array so no zeros is being calculated

# delta_mas = []
# len12 = len(sti.sma(df['Adj Close'], 12))
# len26 = len(sti.sma(df['Adj Close'], 26))
# print('12: ' + str(len12) + ", 26: " + str(len26))
# for i in range(len(sti.sma(df['Adj Close'], 26))):
# 	ma12 = sti.sma(df['Adj Close'], 12)[len12 - i - 1]
# 	ma26 = sti.sma(df['Adj Close'], 26)[len26 - i - 1]
# 	delta_mas.append(ma12 - ma26)
# delta_mas.reverse()
