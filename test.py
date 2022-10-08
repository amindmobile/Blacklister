from typing import Dict

import yaml
from dataclasses import dataclass
from dataclass_factory import Factory


fruits = dict(apple='яблоко', peach='груша')
data = dict(url='gugol.nu', export_file_name='jopa.rsc', fruit=fruits)


@dataclass
class Fruit:
    apple: str
    peach: str


@dataclass
class Bogon:
    url: str
    export_file_name: str
    fruit: Fruit


factory = Factory()
fru = factory.load(fruits, Fruit)
config = factory.load(data, Bogon)

print(config.fruit.peach)






# def read_yaml(path: str) -> dict:
#     with open(path) as f:
#         return yaml.load(f, yaml.FullLoader)
#
#
# print(read_yaml('bogon'))
#
