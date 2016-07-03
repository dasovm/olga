import unittest
from modules.csvimport import CsvImport as Cs
from modules.exeptions import DestinationException, FileNameException


class TestCsvImport(unittest.TestCase, Cs):

    def test_destination_exception(self):
        url = "http://real-chart.finance.yahoo.com/table.csv?s=GOOG&d=5&e=1&f=2016&g=d&a=7&b=19&c=2004&ignore=.csv"
        Cs.set_path(Cs, 'url_too_long_that_should_raise_exception')
        self.assertRaises(DestinationException, Cs.download_csv(csv_url=url))