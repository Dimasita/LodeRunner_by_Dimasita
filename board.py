from graph import Graph


class Board:
    previous_board: str
    current_board: str
    board_side_length: int
    graph: Graph

    def __init__(self, board: str):
        from math import sqrt
        self.current_board = board.lstrip("board=")
        self.board_side_length = int(sqrt(len(self.current_board)))
        self.graph = Graph(self._associate_board_with_coordinates(), self.board_side_length)
        self._update_mutable_fields()

    def __call__(self, board: str):
        self.previous_board = self.current_board
        self.current_board = board.lstrip("board=")
        self.graph.clear()
        self._update_mutable_fields()

    def _associate_board_with_coordinates(self) -> dict[[int, int], str]:
        coords = {}   # Single coord = { (x-coordinate, y-coordinate): sign }
        s = iter(self._get_pure_board_layout())
        for y in range(self.board_side_length):
            for x in range(self.board_side_length):
                coords[(x, y)] = next(s)
        return coords

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

    def _update_mutable_fields(self):
        self.graph.set_hero_position(self._get_hero_position())
        self.graph.set_enemies_positions(self._get_enemies_positions())
        self.graph.set_bags_positions(self._get_bags_positions())

    def _get_hero_position(self) -> tuple[int, int]:
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

    def _get_enemies_positions(self) -> list[[int, int]]:
        coords = list()
        s = iter(self.current_board)
        for y in range(self.board_side_length):
            for x in range(self.board_side_length):
                if next(s) in '⋊⋉⋕⊣⊢)(UЭЄ':
                    coords.append((x, y))
        return coords

    def _get_bags_positions(self) -> list[[int, int]]:
        coords = list()
        s = iter(self.current_board)
        for y in range(self.board_side_length):
            for x in range(self.board_side_length):
                if next(s) in '$&@':
                    coords.append((x, y))
        return coords

    def _calculate_next_step_direction(self, coords: list[(int, int)]) -> str:
        hero_position = self._get_hero_position()
        if coords[0][0] == hero_position[0]:
            i = 0
            while True:
                if coords[i][1] != hero_position[1]:
                    direction = coords[i][1] - hero_position[1]
                    if direction < 0:
                        return 'up'
                    if self._is_wall_block(hero_position[0], hero_position[1] + 1):
                        if (self._is_empty_block(hero_position[0] + 1, hero_position[1] + 1) and not
                                self._is_wall_block(hero_position[0] + 1, hero_position[1])):
                            return 'right'
                        return 'left'
                    return 'down'
                i += 1
        direction = coords[0][0] - hero_position[0]
        if direction > 0:
            if (coords[1][0] == hero_position[0] + 1 and
                    coords[1][1] > hero_position[1] and
                    self._is_wall_block(hero_position[0] + 1, hero_position[1] + 1)):
                return 'act,right'
            return 'right'
        if (coords[1][0] == hero_position[0] - 1 and
                coords[1][1] > hero_position[1] and
                self._is_wall_block(hero_position[0] - 1, hero_position[1] + 1)):
            return 'act,left'
        return 'left'

    def _is_wall_block(self, x: int, y: int) -> bool:
        if self.current_board[y * self.board_side_length + x] == '#':
            return True
        return False

    def _is_empty_block(self, x: int, y: int) -> bool:
        if self.current_board[y * self.board_side_length + x] == ' ':
            return True
        return False

    def is_hero_alive(self) -> bool:
        if 'Ѡ' in self.current_board:
            return False

    def get_next_step_direction(self) -> str:
        coords = self.graph.get_next_step_coordinates(self._get_bags_positions())
        return self._calculate_next_step_direction(coords)
