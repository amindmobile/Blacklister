# https://tutswiki.com/read-write-config-files-in-python/

from configparser import ConfigParser
config_object = ConfigParser()


class Configurator:
    def __init__(self):
        self.ini = config_object.read("config.ini")
        self.links = config_object["LINKS"]

    def write(self):
        # Write to config.ini file
        with open('config.ini', 'w') as config_file:
            config_object.write(config_file)

    def read(self, link_name):
        config_object.read("config.ini")
        try:
            print("'" + link_name + "'" + " link is: {}".format((self.links[str(link_name)])))  # link запрашивать в ини и менять на имя из конфига
        except KeyError:
            print("I don't have information about " + str(link_name).upper() + ", you can add it with 'add' command.")

    def update(self, oldlink, newlink):  # TODO добавить проверку что это URL
        self.links[str(oldlink)] = str(newlink)
        self.write()
        print("URL for" + oldlink + "has been changed to: " + newlink)


# # TODO добавлять и изменять списки через вопрос в консоли
# # Links to the lists (CIDR, ZIP)
# config_object["LINKS"] = {
#     "bogon": "http://list.iblocklist.com/?list=lujdnbasfaaixitgmxpp&fileformat=cidr&archiveformat=zip"
# }
