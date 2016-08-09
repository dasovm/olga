from __future__ import division
import constants
import numpy as np
import pandas as pd
from sklearn import svm, preprocessing


def get_data_set_from_csv(ticker):
    print('Retrieving data about ' + ticker)
    return pd.DataFrame.from_csv('./stock_data/' + ticker + '.csv')


def build_data_set(df):
    print('Preparing data for analyze...')
    X = np.array(df
        .drop('Rating ' + str(constants.RESULT_DAYS) + ' Days', 1)
        .drop('Day of week', 1)
        .drop('Month', 1)
        .drop('Close', 1)
        .values)
    y = (df['Rating ' + str(constants.RESULT_DAYS) + ' Days']
        .replace('BUY', 1)
        .replace('HOLD', 0)
        .replace('SELL', -1)
        .values.tolist())

    print('Preprocessing the data...')
    X = preprocessing.scale(X)
    return X, y


def analyzis(X, y):
    test_size = int(round(len(X) * 0.2))
    print('Size of test-set: ' + str(test_size))

    print('Training the model')
    # Try both with kernel = 'linear' and 'rbf'
    clf = svm.SVC(kernel='linear', C = 1.0)
    clf.fit(X[:-test_size], y[:-test_size])
    # print(clf.predict(X[-1]))
    correct_count = 0

    # print(str(clf.predict(X[-10].reshape(1, -1))[0]) + ', ' + str(y[-10]))
    # print(str(clf.predict(X[-9].reshape(1, -1))) + ', ' + str(y[-9]))
    # print(str(clf.predict(X[-8].reshape(1, -1))) + ', ' + str(y[-8]))
    # print(str(clf.predict(X[-7].reshape(1, -1))) + ', ' + str(y[-7]))
    # print(str(clf.predict(X[-6].reshape(1, -1))) + ', ' + str(y[-6]))
    # print(str(clf.predict(X[-5].reshape(1, -1))) + ', ' + str(y[-5]))
    # print(str(clf.predict(X[-4].reshape(1, -1))) + ', ' + str(y[-4]))
    # print(str(clf.predict(X[-3].reshape(1, -1))) + ', ' + str(y[-3]))
    # print(str(clf.predict(X[-2].reshape(1, -1))) + ', ' + str(y[-2]))
    # print(str(clf.predict(X[-1].reshape(1, -1))) + ', ' + str(y[-1]))

    print('Testing the model')
    for x in range(1, test_size + 1):
        # print(str(clf.predict(X[-x].reshape(1, -1))[0]) + ', ' + str(y[-x]))
        if clf.predict(X[-x].reshape(1, -1))[0] == y[-x]:
            correct_count += 1

    print ('Accuracy: ' + str(round((correct_count / test_size) * 100, 2)) + '%\n')
