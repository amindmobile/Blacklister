import ipaddress
from zipfile import ZipFile
from io import BytesIO
import requests
import os.path


archive = 'http://list.iblocklist.com/?list=lujdnbasfaaixitgmxpp&fileformat=cidr&archiveformat=zip'


# Download archive from url
def download(url):
    response = requests.get(url)
    stream = BytesIO(response.content)  # Output as stream!
    return stream


# Read the file inside archive
def get_zip_contents(stream):
    with ZipFile(stream) as zip_file:
        archived_file_name = zip_file.namelist()[0]
        with zip_file.open(archived_file_name) as unzipped_file:
            return unzipped_file.readlines()


# Cleanse trash
def clean(contents):
    filtered_ip = set()
    decoded_ip = [ip_address.decode().strip() for ip_address in contents]
    # print(decoded_ip)
    for ip in decoded_ip:
        print(ip)

    # i = 0
    # while i < len(decoded_ip):
    #     print(decoded_ip[i])
    #     i += 1

    # for ip in decoded_ip:
    #     # print(ip)
    #     try:
    #         if ipaddress.ip_network(ip):
    #             filtered_ip.add(ip)
    #     except ValueError:
    #         continue
    #     return list(filtered_ip)  # stream


# Create firewall rules for Mikrotik
def get_file(list_name, cleaned_content, export_file):
    firewall_string = f'ip firewall address-list add list={list_name.upper()} address='
    with open(export_file, 'w') as file:
        for subnet in cleaned_content:
            mikrotik_firewall_string = firewall_string+subnet
            file.write('%s\n' % mikrotik_firewall_string)
    if os.path.exists(export_file):
        print(f'\nFile: {export_file} was exported and ready to use.')


def test_clean():
    for i in clean(get_zip_contents(download(archive))):
        print(i)
# get_file('bogon', clean(get_zip_contents(download(archive))), 'bogon.txt')

# test_clean()


print(clean(get_zip_contents(download(archive))))
