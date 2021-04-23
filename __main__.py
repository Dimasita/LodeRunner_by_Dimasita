import logging
import random

from internals.actions import LoderunnerAction
from internals.board import Board
from game_client import GameClient

logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s", level=logging.INFO)


def turn(gcb: Board):
    action_id = random.randint(0, len(LoderunnerAction) - 1)
    return list(LoderunnerAction)[action_id]


def main():
    gcb = GameClient("https://dojorena.io/codenjoy-contest/board/player/dojorena390?code=7695259786981933783")
    gcb.run(turn)


if __name__ == "__main__":
    main()
