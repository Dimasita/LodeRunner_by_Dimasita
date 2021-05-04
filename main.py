from connect import GameClient
from board import Board


def calculate_action(board: Board) -> str:
    direction = board.get_next_step_direction()
    return direction


if __name__ == '__main__':
    GameClient('ws://localhost:3000', calculate_action)
