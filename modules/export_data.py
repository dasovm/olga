import os
import constants as pc


def export_to_csv(df, ticker):
    path = pc.STOCK_DATA
    if not os.path.exists(path):
        os.makedirs(path)
    df.to_csv(path + ticker + '.csv')
    print(str(len(df.index)) + " rows of data has been saved to: " + ticker + '.csv')
