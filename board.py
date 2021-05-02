class Board:
    board_layout: dict[[int, int], str]
    previous_board: str
    current_board: str
    board_side_length: int

    def __init__(self, board: str):
        from math import sqrt
        self.current_board = board.lstrip("board=")
        self.board_side_length = int(sqrt(len(self.current_board)))
        self._associate_board_with_coordinates()

    def __call__(self, board: str):
        self.previous_board = self.current_board
        self.current_board = board.lstrip("board=")

    def _associate_board_with_coordinates(self):
        coords = {}   # Single coord = { (x-coordinate, y-coordinate): sign }
        s = iter(self._get_pure_board_layout())
        for y in range(self.board_side_length):
            for x in range(self.board_side_length):
                coords[(x, y)] = next(s)
        self.board_layout = coords

    def _get_pure_board_layout(self) -> str:
        board = self.current_board

        for ch in ['Q', 'Y', 'U']:
            if ch in board:
                board = board.replace(ch, 'H')

        for ch in ['<', '>', '{', '}', 'Э', 'Є']:
            if ch in board:
                board = board.replace(ch, '~')

        for ch in ['«', '»', '$', '&', '@', ']', '[', ')', '(', '⊛', 'S', '◄', '►']:
            if ch in board:
                board = board.replace(ch, ' ')

        return board

    def is_hero_alive(self) -> bool:
        if 'Ѡ' in self.current_board:
            return False

    def can_drill_block(self, x: int, y: int) -> bool:
        if self.board_layout[(x, y)] == '#':
            return True
        return False

    def get_bags_positions(self) -> list[[int, int]]:
        coords = list()
        s = iter(self.current_board)
        for y in range(self.board_side_length):
            for x in range(self.board_side_length):
                if next(s) in '$&@':
                    coords.append((x, y))
        return coords

    def get_enemies_positions(self) -> list[[int, int]]:
        coords = list()
        s = iter(self.current_board)
        for y in range(self.board_side_length):
            for x in range(self.board_side_length):
                if next(s) in '⋊⋉⋕⊣⊢)(UЭЄ':
                    coords.append((x, y))
        return coords

    def get_hero_position(self) -> tuple[int, int]:
        index: int
        for i in '◄►ЯRY][{}⊰⊱⍬⊲⊳⊅⊄⋜⋝Ѡ':
            index = self.current_board.find(i)
            if index != -1:
                break
        y = 0
        while index >= self.board_side_length:
            index -= self.board_side_length
            y += 1
        return index, y
