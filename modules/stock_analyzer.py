from __future__ import division
import constants
import numpy as np
import stock_indicators as si
from sklearn import svm, preprocessing, ensemble


def build_data_set(df):
    print('Preparing data for analyze...')
    X = np.array(df
        .drop('Rating ' + str(constants.RESULT_DAYS) + ' Days', 1)
        .drop('Day of week', 1)
        .drop('Month', 1)
        .drop('Close', 1)
        .drop('Buy', 1)
        .drop('Result', 1)
        .values)
    # y = (df['Rating ' + str(constants.RESULT_DAYS) + ' Days']
    #     .replace('BUY', 1)
    #     .replace('HOLD', 0)
    #     .replace('SELL', -1)
    #     .values.tolist())
    y = (df['Buy'].values.tolist())

    print('Preprocessing the data...')
    X = preprocessing.scale(X)
    return X, y


def train_and_test(X, y, percents):
    test_size = int(round(len(X) * 0.05))
    print('Size of test-set: ' + str(test_size))

    print('Training the model')
    # Try both with kernel = 'linear' and 'rbf'
    # clf = svm.SVC(kernel='linear', C = 0.01)
    clf = svm.LinearSVC(C = 1.0, dual = False)
    # clf = ensemble.RandomForestClassifier(n_jobs=-1,
    #     n_estimators=200,
    #     criterion='entropy')
    clf.fit(X[:-test_size], y[:-test_size])

    correct_count = 0
    stock_percent = 0
    result_percent = 0
    is_bougth = False

    print('Testing the model')
    print 'Features: ' + str(len((X[-1]).reshape(1, -1)[0]))
    for x in range(1, test_size + 1):
        if clf.predict(X[-x].reshape(1, -1))[0] == 1:
            is_bougth = True
        elif clf.predict(X[-x].reshape(1, -1))[0] == 0:
            is_bougth = False
        
        if clf.predict(X[-x].reshape(1, -1))[0] == y[-x]:
            correct_count += 1
        stock_percent += percents[-x]
        if is_bougth:
            result_percent += percents[-x]
        print 'Guessed: ', str(clf.predict(X[-x].reshape(1, -1))[0]), 'Right: ', str(y[-x]), 'Result:', result_percent

    print ('Accuracy: ' + str(round((correct_count / test_size) * 100, 2)) + '%\n')
    print ('Result: ' + str(result_percent - stock_percent) + ' difference from stock.')


def predict(X, y, last_day_df, ticker = ''):
    print('')
    last_day = np.array(last_day_df
        .drop('Day of week', 1)
        .drop('Month', 1)
        .drop('Close', 1)
        .values)
    clf = svm.LinearSVC(C = 1.0, dual = False)
    clf.fit(X, y)
    prediction = si.get_rating_from_digit(clf.predict(last_day.reshape(1, -1))[0])
    print(prediction + ' ' + ticker + ' @ price ' + str(last_day_df['Close'].values[0]))
    return prediction