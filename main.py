
from blacklister import clean, get_zip_contents, download, archive, get_file
from configurator import Configurator

# TODO сделать класс в engine
# TODO вместо импортов использовать методы класса из его объекта

# temporary short config
# result = clean(get_zip_contents(download(archive)))
# list_name = 'bogon'
# export_file_name = 'bogon.rsc'
#
# get_file(list_name, result, export_file_name)
#

con = Configurator()


# con.update('bogon', 'bogon1')
# con.read("bogon")

con.add("123")
