from urllib import request
from olga.exeptions import DestinationException


class CsvImport:

    def __init__(self):
        pass

    goog_url = "http://real-chart.finance.yahoo.com/table.csv?s=GOOG&d=5&e=1&f=2016&g=d&a=7&b=19&c=2004&ignore=.csv"
    destination_url = ""

    def download_csv(self, csv_url):
        response = request.urlopen(csv_url)
        csv = response.read()
        csv_str = str(csv)
        lines = csv_str.split("\\n")
        self.destination_url = self.get_destination_path()
        fx = open(self.destination_url, 'w')
        for line in lines:
            fx.write(line + "\n")
        fx.close()

    def get_destination_path(self):
        if self.destination_url == "":
            raise DestinationException('NotFound')
        return self.destination_url

    def set_destination_path(self, url):
        if len(url) < 10:
            raise DestinationException('Invalid')
        self.destination_url = url
