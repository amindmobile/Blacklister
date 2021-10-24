import argparse
from engine import Blocklister

parser = argparse.ArgumentParser(description='Create file with firewall rules.')
parser.add_argument('list', type=str.lower, help='Name of the blacklist')
args = parser.parse_args()
download = Blocklister()
download.choose(args.list)





















# loguru


# if __name__ == '__main__':
#     from timeit import Timer
#     t = Timer(lambda: test('bogon1.zip'))
#     print(t.timeit(number=10))


# TODO: из Synology добавить обработчик в роутер. Проверять на объединение в подсети.
