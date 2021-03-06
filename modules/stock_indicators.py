import numpy as np
import pandas as pd
import talib
from collections import deque
import constants


def rsi(prices, n=14):
    deltas = np.diff(prices)
    seed = deltas[:n + 1]
    up = seed[seed >= 0].sum() / n
    down = -seed[seed < 0].sum() / n
    rs = up / down
    rsi = np.zeros_like(prices)
    rsi[:n] = 100. - 100. / (1. + rs)

    for i in range(len(prices)):
        delta = deltas[i - 1]
        if delta >= 0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta

        up = (up * (n - 1) + upval) / n
        down = (down * (n - 1) + downval) / n

        rs = up / down
        rsi[i] = 100. - 100. / (1. + rs)

    return rsi


def sma(values, window):
    weights = np.repeat(1.0, window) / window
    smas = np.convolve(values, weights, 'valid')
    smas = smas[::-1]  # numpy vector reverse
    zeros = [0] * (len(values) - len(smas))
    zeros = np.array(zeros)
    smas = np.append(smas, zeros)
    smas = smas[::-1]  # reversing it back
    return smas


def ema(values, window):
    weights = np.exp(np.linspace(-1., 0., window))
    weights /= weights.sum()

    a = np.convolve(values, weights, mode='full')[:len(values)]
    a[:window] = a[window]
    return a


def macd(values, slow=26, fast=12):
    ema_slow = ema(values, slow)
    ema_fast = ema(values, fast)
    return ema_fast - ema_slow


def macd_signal(values, signal=9):
    ema_signal = ema(values, signal)
    return ema_signal


def stochastic(high, low, close, time=14):
    l, h = low.rolling(time).min(), high.rolling(time).max()
    k = 100 * (close - l) / (h - l)
    return k, sma(k, 3)


def aroon(high, low, time=25):
    return np.array(talib.AROON(high, low))


def cci(high, low, close, time=20):
    return np.array(talib.CCI(high, low, close, time))


def adx(high, low, close, time=14):
    return np.array(talib.ADX(high, low, close))


def mom(close):
    return np.array(talib.MOM(close))


def diff(values1, values2):
    return values1 - values2


def delta(values, time_difference):
    old_values = np.roll(values, time_difference)
    return values - old_values


def delta_percent(values, time_difference):
    old_values = np.roll(values, time_difference)
    return ((values - old_values) / old_values) * 100


def result_percent(values, time_difference):
    result_values = np.roll(values, -time_difference)
    return((result_values - values) / values) * 100


def get_rating_from_result(result):
    rating_list = []
    for i, r in np.ndenumerate(result):
        if (r >= constants.MIN_BUY):
            rating_list.append('BUY')
        elif (r <= constants.MIN_SELL):
            rating_list.append('SELL')
        else:
            rating_list.append('HOLD')
    return np.array(rating_list)


def get_rating_from_digit(digit):
    if digit == 1:
        return 'BUY'
    elif digit == 0:
        return 'HOLD'
    elif digit == -1:
        return 'SELL'
    else:
        return 'WHAT'
