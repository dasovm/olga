import numpy as np
from collections import deque


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


def diff_macd(macd, macd_signal):
	return macd - macd_signal


def delta(values, time_difference):
	old_values = np.roll(values, time_difference)
	return values - old_values
