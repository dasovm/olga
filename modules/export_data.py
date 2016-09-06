import os
import constants as pc


def export_to_csv(df, ticker, path=pc.STOCK_DATA):
    if not os.path.exists(path):
        os.makedirs(path)
    df.to_csv(path + ticker + '.csv')
    print(str(len(df.index)) + " rows of data has been saved to: " + ticker + '.csv')


def export_log_to_csv(df, date, path=pc.TRANSACTION_LOG):
    if not os.path.exists(path):
        os.makedirs(path)
    df.to_csv(path + str(date) + '.csv')
    print(str(len(df.index)) + " rows of data has been saved to: " + str(date) + '.csv')


def export_stock_list(stock_list, file_name):
    file = open(file_name, 'w')
    for stock in stock_list:
        file.write(stock + '\n')
    file.close()