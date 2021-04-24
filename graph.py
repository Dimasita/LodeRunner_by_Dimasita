class Edge:

    verticals = []
    horizontals = []

    def empty(self) -> None:
        self.verticals = []
        self.horizontals = []

    def add_horizontal(self, points: set[(int, int)]) -> None:
        self.horizontals.append(self.Horizontal(points))

    def add_vertical(self, points: set[(int, int)], digging_zones: set[(int, int)], endpoint=None) -> None:
        self.verticals.append(self.Vertical(points, endpoint, digging_zones, self))

    def set_intersecting_points_for_horizontal(self) -> None:
        for h_index, horizontal in enumerate(self.horizontals):
            for v_index, vertical in enumerate(self.verticals):
                if vertical.end_point is not None:  # if not ladder
                    if vertical.end_point in horizontal.points:
                        self.horizontals[h_index].intersecting_points.append((v_index, vertical.end_point))
                else:
                    if not horizontal.points.isdisjoint(vertical.points):
                        for p in horizontal.points.intersection(vertical.points):
                            self.horizontals[h_index].intersecting_points.append((v_index, p))

    def set_intersecting_points_for_vertical(self, vertical: set[(int, int)]) -> list[(int, (int, int))]:
        e_points = list()
        for index, horizontal in enumerate(self.horizontals):
            if not horizontal.points.isdisjoint(vertical):
                e_points.append((index, horizontal.points.intersection(vertical).pop()))
        return e_points

    def set_bags_positions(self, bags: list[tuple[int, int]]) -> None:
        for bag in bags:
            for index, vertical in enumerate(self.verticals):
                if bag in vertical.points:
                    self.verticals[index].bags_points.append(bag)
                    break

    def set_hero_position(self, coords: tuple[int, int]) -> None:
        for index, horizontal in enumerate(self.horizontals):
            if coords in horizontal.points:
                self.horizontals[index].has_hero = True
                self.horizontals[index].hero_coords = coords[0]
                break
        else:
            offset = 0
            while True:
                is_needed_break = False
                lst = list(coords)
                lst[1] += 1
                offset += 1
                for index, horizontal in enumerate(self.horizontals):
                    if tuple(lst) in horizontal.points:
                        self.horizontals[index].hero_offset = offset
                        self.horizontals[index].hero_coords.append(coords[0])
                        self.horizontals[index].has_hero = True
                        is_needed_break = True
                        break
                if is_needed_break:
                    break

    def set_enemies_positions(self, coords: list[tuple[int, int]]) -> None:
        for coord in coords:
            for index, horizontal in enumerate(self.horizontals):
                if coord in horizontal.points:
                    self.horizontals[index].enemies_coords.append(coord[0])
                    self.horizontals[index].has_enemies = True
                    break
            else:
                offset = 0
                while True:
                    is_needed_break = False
                    lst = list(coord)
                    offset += 1
                    lst[1] += offset
                    for index, horizontal in enumerate(self.horizontals):
                        if tuple(lst) in horizontal.points:
                            c = str(len(str(offset))) + str(offset) + str(coord[0])
                            self.horizontals[index].enemies_coords.append(-(int(c)))
                            self.horizontals[index].has_enemies = True
                            is_needed_break = True
                            break
                    if is_needed_break: 
                        break

    class Horizontal:
        points: set[(int, int)]
        intersecting_points: list[(int, (int, int))]    # end points of all verticals
        has_hero: bool
        hero_coords: int
        hero_offset: int
        has_enemies: bool
        enemies_coords: list[int]

        def __init__(self, points: set[(int, int)]):
            self.points = points
            self.intersecting_points = list()
            self.has_enemies = False
            self.has_hero = False
            self.enemies_coords = list()
            self.hero_offset = 0

    class Vertical:
        points: set[(int, int)]
        intersecting_points: list[(int, (int, int))]
        end_point: (int, int)
        bags_points: list[(int, int)]
        digging_zones: set[(int, int)]

        def __init__(self, points: set[(int, int)], endpoint: (int, int),
                     digging_zones: set[(int, int)], parent):
            self.points = points.copy()
            self.end_point = endpoint
            self.intersecting_points = parent.set_intersecting_points_for_vertical(points)
            self.bags_points = list()
            self.digging_zones = digging_zones
