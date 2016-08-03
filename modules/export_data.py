import os


def export_to_csv(df, ticker):
	if not os.path.exists('./stock_data/'):
		os.makedirs('./stock_data/')
	df.to_csv('./stock_data/' + ticker + '.csv')
	print(str(len(df.index)) + " rows of data has been saved to: " + ticker + '.csv')
