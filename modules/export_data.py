import os
import path_constant as pc


def export_to_csv(df, ticker):
    if not os.path.exists(pc.get_stock_data_path()):
        os.makedirs(pc.get_stock_data_path())
    df.to_csv(pc.get_stock_data_path() + ticker + '.csv')
    print(str(len(df.index)) + " rows of data has been saved to: " + ticker + '.csv')
