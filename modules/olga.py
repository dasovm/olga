import stock_analyzer as analyzer
import data_receiver as receiver
import export_data as exporter
import import_data as importer

"""
Main class
"""

ticker = 'AAK.ST'


def main():
    symbols = importer.get_symbol_list()
    stock_count = len(symbols.splitlines())

    for symbol in symbols.splitlines():
        df, last_day_data = receiver.get_stock_data(symbol + '.ST')
        # ed.export_to_csv(df, symbol + '.ST')
        df = receiver.get_stock_data(symbol + '.ST')
        exporter.export_to_csv(df, symbol + '.ST')
        stock_count -= 1
        # X, y = sa.build_data_set(sa.get_data_set_from_csv(symbol + '.ST'))
        X, y = analyzer.build_data_set(df)
        # sa.train_and_test(X, y)
        analyzer.predict(X, y, last_day_data, symbol)
        print(str(stock_count) + ' stocks left.')
        print '----------\n'
        # break


if __name__ == '__main__':
    main()
