import constants as pc
import pandas as pd


def get_symbol_list():
    return import_text_file_to_string('./symbol_list.txt')


def import_text_file_to_string(path):
    file = open(path, 'r')
    return file.read()


def get_data_set_from_csv(ticker, path=pc.STOCK_DATA):
    print('Retrieving data about ' + ticker)
    return pd.DataFrame.from_csv(path + ticker + '.csv')
