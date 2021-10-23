import argparse
from engine import Blocklister

parser = argparse.ArgumentParser(description='Create file with firewall rules.')
parser.add_argument('list', type=str.lower, help='Name of the blacklist')
args = parser.parse_args()
download = Blocklister()

if args.list == 'drop':
    download.choose('drop')
elif args.list == 'moon':
    print('\n No, no! "Moon was just an example. You must use real name of the list."')
elif args.list == 'bogon':
    print('\n The blacklist "bogon" is not implemented yet.')

else:
    print('\nFor use please enter: python main.py list_name')
    print('\nFor example: python main.py moon')


# loguru




# if __name__ == '__main__':
#     from timeit import Timer
#     t = Timer(lambda: test('bogon1.zip'))
#     print(t.timeit(number=10))


# TODO: из Synology добавить обработчик в роутер. Проверять на объединение в подсети.
