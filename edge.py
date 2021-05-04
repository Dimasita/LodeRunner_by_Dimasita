from typing import Optional


class Edge:
    points: set[(int, int)]
    intersecting_points: list[(int, (int, int))]


class Horizontal(Edge):
    has_hero: bool
    hero_x_coord: Optional[int]
    hero_y_offset: Optional[int]
    has_enemies: bool
    enemies_x_coord: Optional[list[int]]
    enemies_y_offset: Optional[list[int]]

    def __init__(self, points: set[(int, int)]):
        self.points = points
        self.intersecting_points = list()
        self.has_enemies = False
        self.has_hero = False


class Vertical(Edge):
    end_point: (int, int)
    digging_zones: set[(int, int)]
    bags_points: Optional[list[(int, int)]]

    def __init__(self, points: set[(int, int)], digging_zones: set[(int, int)], endpoint: (int, int) = None):
        self.points = points.copy()
        self.intersecting_points = list()
        self.end_point = endpoint
        self.digging_zones = digging_zones
        self.bags_points = list()
