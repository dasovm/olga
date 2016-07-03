from urllib import request

from modules.exeptions import DestinationException, FileNameException


class CsvImport:

    def __init__(self):
        self.destination_path = ''

    def download_csv(self, csv_url):
        response = request.urlopen(url=csv_url)
        csv = response.read()
        csv_str = str(csv)
        lines = csv_str.split("\\n")
        self.write_data(lines)

    def write_data(self, data):
        fx = open(self.file_name, 'w')
        for line in data:
            fx.write(line + "\n")
        fx.close()

    @property
    def path(self):
        if self.destination_path == '':
            raise DestinationException('NotFound')
        return self.destination_path

    def set_path(self, new_path):
        if len(new_path) > 10:
            raise DestinationException('Invalid')
        self.destination_path = new_path

    @property
    def file_name(self, name):
        if len(name) < 0:
            raise FileNameException('Not valid file name')
        return name + '.csv'
