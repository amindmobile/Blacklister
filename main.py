import argparse
from engine import Blacklister
import yaml

# parser = argparse.ArgumentParser(description='Create file with firewall rules.')
# parser.add_argument('list', type=str.lower, help='Name of the blacklist')
# args = parser.parse_args()
# download = Blacklister()
# download.choose(args.list)


def read_yaml(path: str) -> dict:
    with open(path) as file:
        return yaml.load(file, yaml.FullLoader)

# def read_yaml(file):
#     with open(file, "r") as stream:
#         try:
#             print(yaml.safe_load(stream))
#         except yaml.YAMLError as exc:
#             return exc


config = read_yaml('settings.yaml')

print(config)
