import ipaddress
from zipfile import ZipFile
import configparser
from io import BytesIO
import requests

config = configparser.ConfigParser()
config.read('settings.ini')


class Blocklister:
    def __init__(self):
        self.url = ''
        self.export = ''
        self.list_name = ''

    def _get_url(self):
        response = requests.get(self.url)
        archive = BytesIO(response.content)
        return archive

    # Read file inside archive
    def _get_zip_contents(self):
        with ZipFile(self._get_url()) as zip_file:
            archived_file_name = zip_file.namelist()[0]
            with zip_file.open(archived_file_name) as unzipped_file:
                return unzipped_file.readlines()

    # Cleanse trash
    def _decode_ip(self):
        decoded_ip = [ip_address.decode().strip() for ip_address in self._get_zip_contents()]
        filtered_ip = set()
        for ip in decoded_ip:
            try:
                if ipaddress.ip_network(ip):
                    filtered_ip.add(ip)
            except ValueError:
                continue
        return list(filtered_ip)

    # Create firewall rules for Mikrotik
    def _get_file(self, list_name):
        firewall_string = 'ip firewall address-list add list=DROP address='
        with open(self.export, 'w') as mikrotik:
            for subnet in self._decode_ip():
                mikrotik_firewall_string = firewall_string+subnet
                mikrotik.write('%s\n' % mikrotik_firewall_string)

    def choose(self, list_name):
        if list_name == 'bogon':
            self.list_name = list_name
            self.url = config['bogon']['url']
            self.export = config['bogon']['export_file_name']
            self._get_file(list_name)

        elif list_name == 'drop':
            self.list_name = list_name
            self.url = config['drop']['url']
            self.export = config['drop']['export_file_name']
            self._get_file(list_name)


download = Blocklister()
download.choose('drop')







# if __name__ == '__main__':
#     from timeit import Timer
#     t = Timer(lambda: test('bogon1.zip'))
#     print(t.timeit(number=10))


# TODO: из Synology добавить обработчик в роутер. Проверять на объединение в подсети.
