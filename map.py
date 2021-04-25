from math import sqrt


class Map:
    base_map_string: str
    reformed_map_string: str
    map_side_length: int

    def set_base_map_string(self, map_str: str):
        self.base_map_string = map_str.lstrip("board=")
        self.map_side_length = int(sqrt(len(self.base_map_string)))
        self._reformat_map_on_start()
        return self.base_map_string

    def is_hero_alive(self) -> bool:
        if 'Ѡ' in self.base_map_string:
            return False

    @staticmethod
    def ladders_reform(map_str: str) -> str:
        for ch in ['Q', 'Y', 'U']:
            if ch in map_str:
                map_str = map_str.replace(ch, 'H')
        return map_str

    @staticmethod
    def pipe_reform(map_str: str) -> str:
        for ch in ['<', '>', '{', '}', 'Э', 'Є']:
            if ch in map_str:
                map_str = map_str.replace(ch, '~')
        return map_str

    @staticmethod
    def void_reform(map_str: str) -> str:
        for ch in ['«', '»', '$', '&', '@', ']', '[', ')', '(', '⊛', 'S', '◄', '►']:
            if ch in map_str:
                map_str = map_str.replace(ch, ' ')
        return map_str

    def _reformat_map_on_start(self) -> None:
        self.reformed_map_string = self.ladders_reform(self.pipe_reform(self.void_reform(self.base_map_string)))

    def associate_map_with_coordinates(self) -> dict[[int, int], str]:
        coords = {}   # Single coord = { (x-coordinate, y-coordinate): sign }
        s = iter(self.reformed_map_string)
        for y in range(0, self.map_side_length):
            for x in range(0, self.map_side_length):
                coords[(x, y)] = next(s)
        return coords

    def get_bags_positions(self) -> list[[int, int]]:
        coords = list()
        s = iter(self.base_map_string)
        for y in range(self.map_side_length):
            for x in range(self.map_side_length):
                if next(s) == '$&@':
                    coords.append((x, y))
        return coords

    def get_enemies_positions(self) -> list[[int, int]]:
        coords = list()
        s = iter(self.base_map_string)
        for y in range(self.map_side_length):
            for x in range(self.map_side_length):
                if next(s) in '⋊⋉⋕⊣⊢)(UЭЄ':
                    coords.append((x, y))
        return coords

    def get_hero_position(self) -> tuple[int, int]:
        index: int
        for i in '◄►ЯRY][{}⊰⊱⍬⊲⊳⊅⊄⋜⋝Ѡ':
            index = self.base_map_string.find(i)
            if index != -1:
                break
        y = 0
        while index >= self.map_side_length:
            index -= self.map_side_length
            y += 1
        return index, y
