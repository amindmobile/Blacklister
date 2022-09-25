import ipaddress
from zipfile import ZipFile
import configparser
from io import BytesIO
import requests
import os.path
import yaml


def read_yaml(path: str) -> dict:
    with open(path) as f:
        return yaml.load(f, yaml.FullLoader)


class Downloader:
    # Download archive from url
    def __init__(self, url):
        self.url = url

    def get_url(self):
        response = requests.get(self.url)
        archive = BytesIO(response.content)  # Output as stream!
        return archive


class Unarchiver:
    # Read the file inside archive

    def __init__(self, archive_name):
        self.archivename = archive_name

    def _get_zip_contents(self):
        with ZipFile(self.archivename) as zip_file:
            archived_file_name = zip_file.namelist()[0]
            with zip_file.open(archived_file_name) as unzipped_file:
                return unzipped_file.readlines()


class Cleaner:
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
    def get_file(self, list_name):
        firewall_string = f'ip firewall address-list add list={self.list_name.upper()} address='
        with open(self.export, 'w') as mikrotik:
            for subnet in self._decode_ip():
                mikrotik_firewall_string = firewall_string+subnet
                mikrotik.write('%s\n' % mikrotik_firewall_string)
        if os.path.exists(self.export):
            print(f'\nFile: {self.export} was exported and ready to use.')

