from connect import GameClient
from funcs import new_msg


def main():
    gcb = GameClient('ws://localhost:3000', new_msg)


if __name__ == '__main__':
    main()
