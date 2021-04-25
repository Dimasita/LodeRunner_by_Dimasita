from decorators import benchmark
from connect import GameClient
from graph import Edge
from map import Map


def main():
    # gcb = GameClient('https://dojorena.io/codenjoy-contest/board/player/dojorena390?code=7695259786981933783')
    gcb = GameClient('ws://localhost')


if __name__ == '__main__':
    main()
