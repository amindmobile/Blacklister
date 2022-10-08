# loguru


# if __name__ == '__main__':
#     from timeit import Timer
#     t = Timer(lambda: test('bogon1.zip'))
#     print(t.timeit(number=10))


# TODO: из Synology добавить обработчик в роутер. Проверять на объединение в подсети.


было бы эффективнее отделить choose, не делать config глобалом, сделать listnames глобальной константой (это нормально, константы называются капсом).
Тогда получится что-то такое
class Exporter:
  def __init__(self, url, export, list_name):
    ...

def choose(config, list_name):
  if list_name in LISTNAMES:
    some_list = config[list_name]
    return Exporter(some_list["url"], ...)
  ...

# import yaml
#
#
# def read_yaml(path: str) -> dict:
#   with open(path) as f:
#     return yaml.load(f, yaml.FullLoader)
# Потом получившееся можно ещё не плохо в датаклассы конфига сложить, но это так…


# YAML
# something:
#   listnames:
#     - bogon
#     - drop
#     - badpeers
# Ну, или просто
# listnames: [bogon, drop, badpeers]



# @dataclasses.dataclass
# class Exporter:
#   url: str
#   export: str
#   list_name: str
#
# Exporter(url, export, list_name)




Если это конфиг, то у меня примерно так:
config.py
@dataclass
class BotConfig:
  token: str


@dataclass
class ApiConfig:
  host: str
  port: int


@dataclass
class Config:
  debug: bool
  bot: BotConfig
  api: ApiConfig


# TODO Сделать свой CALENDY

И потом в это загружаю результат read_yaml


Пугает, что там за "основной файл с классами". Так-то всё разделить стоило бы)


У меня обычно config.py в котором находится датакласс конфига с методом для чтения конфига



dataclass'ы нужны для того чтобы IDE лучше понимала типы данные в полях и подсказывала возможные аттрибуты + чтобы можно было красиво через точку обращаться: config.bot.token
YAML с ним никак не связан, это мог бы быть .JSON, .cfg или что-нибудь ещё, просто перед созданием датаклассов, нужно преобразовать всё в словарь и потом уже передать датаклассам. Если без dataclass_factory то
Config(data["..."], data["..."], ...)

# TODO
@dataclass
class A
    dct: dict[str, dict[int, float]]




    # def choose(self, list_name):
    #     listnames = ('bogon', 'drop')
    #     # istnames = config[listnames]
    #
    #     if list_name in listnames:
    #         self.list_name = list_name
    #         self.url = config[list_name]['url']
    #         self.export = config[list_name]['export_file_name']
    #         self.get_file(list_name)
    #
    #     else:
    #         print(f'\nI cant work with list "{list_name}" yet.')
    #         print('For use please enter: python main.py list_name')
    #         print(f'Currently implemented lists: {listnames}')



# parser = argparse.ArgumentParser(description='Create file with firewall rules.')
# parser.add_argument('list', type=str.lower, help='Name of the blacklist')
# args = parser.parse_args()
# download = Blacklister()
# download.choose(args.list)


# def read_yaml(file):
#     with open(file, "r") as stream:
#         try:
#             print(yaml.safe_load(stream))
#         except yaml.YAMLError as exc:
#             return exc


# def read_yaml(path: str) -> dict:
#     with open(path) as file:
#         return yaml.load(file, yaml.FullLoader)




# bogon = 'http://list.iblocklist.com/?list=lujdnbasfaaixitgmxpp&fileformat=cidr&archiveformat=zip'
# url = bl.get_file(bogon, 'Bogon')

# config = read_yaml('settings.yaml')

# print(config)
