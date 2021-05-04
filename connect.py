import websocket
from board import Board
from typing import Optional

websocket.default_timeout = 3600


class GameClient:
    board: Optional[Board]
    get_action: callable([[Board], str])

    def __init__(self, url, func):
        self.board = None
        self.get_action = func

        self.socket = websocket.WebSocketApp(
            url,
            on_message=lambda ws, msg: self._on_message(ws, msg),
            on_error=lambda ws, err: self._on_error(ws, err),
            on_close=lambda ws, err: self._on_close(ws),
            on_open=lambda ws, err: self._on_open(ws)
        )
        self.socket.run_forever()

    def _on_message(self, ws, message):
        if self.board is None:
            self.board = Board(message)
        else:
            self.board(message)
        self._send(self.get_action(self.board))

    def _send(self, msg):
        self.socket.send(msg)

    @staticmethod
    def _on_error(ws, error):
        print(f'Something was wrong!\n{error}')

    @staticmethod
    def _on_open(ws):
        print(f'Connection successfully established! {ws}')

    @staticmethod
    def _on_close(ws):
        print(f'Connection closed! {ws}')
