import argparse
from engine import Blacklister

parser = argparse.ArgumentParser(description='Create file with firewall rules.')
parser.add_argument('list', type=str.lower, help='Name of the blacklist')
args = parser.parse_args()
download = Blacklister()
download.choose(args.list)
