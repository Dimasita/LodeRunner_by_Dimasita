from collections import deque
from edge import Horizontal, Vertical


class Graph:
    horizontals: list[Horizontal]
    verticals: list[Vertical]

    def __init__(self, coords: dict[[int, int], str], board_side_length: int):
        self._create_list_of_horizontals(coords, board_side_length)
        self._create_list_of_verticals(coords, board_side_length)
        self._set_intersecting_points_for_horizontals()
        self._set_intersecting_points_for_verticals()

    def _create_list_of_horizontals(self, coords: dict[[int, int], str], board_side_length: int) -> None:
        self.horizontals = list()
        edge = set()

        real_board_side_length = board_side_length - 1
        for y in range(board_side_length):
            for x in range(real_board_side_length):
                if coords[(x, y)] == '#' or coords[(x, y)] == '☼':
                    if len(edge) > 0:
                        self.horizontals.append(Horizontal(edge.copy()))
                        edge.clear()
                    else:
                        if (coords[(x, y)] == '#' and
                                (coords[(x, y + 1)] == '#' or coords[(x, y + 1)] == '☼') and
                                (coords[(x, y - 1)] == '#' or coords[(x, y - 1)] == '☼')):
                            self.horizontals.append(Horizontal(edge.copy()))
                            edge.clear()
                    continue

                if coords[(x, y + 1)] != ' ' or coords[(x, y)] == 'H' or coords[(x, y)] == '~':
                    edge.add((x, y))
                    continue

                if len(edge) > 0:
                    edge.add((x, y))
                    self.horizontals.append(Horizontal(edge.copy()))
                    edge.clear()

                if (coords[(x + 1, y)] != '#' and coords[(x + 1, y)] != '☼' and
                        (coords[(x + 1, y + 1)] != ' ' or
                         (coords[(x + 1, y)] == 'H' or coords[(x + 1, y)] == '~'))):
                    edge.add((x, y))
                    x += 1
                    edge.add((x, y))

    def _create_list_of_verticals(self, coords: dict[[int, int], str], board_side_length: int) -> None:
        self.verticals = list()
        edge = set()
        digging_zones = set()
        for x in range(board_side_length):
            for y in range(board_side_length):

                if coords[(x, y)] == 'H':
                    if coords[(x, y - 1)] == ' ' or coords[(x, y - 1)] == '~':
                        edge.add((x, y - 1))

                    edge.add((x, y))
                    if coords[(x, y + 1)] != 'H':
                        self.verticals.append(Vertical(edge.copy(), digging_zones.copy()))
                        edge.clear()
                        digging_zones.clear()
                    continue

                if coords[(x, y)] == ' ':
                    if coords[(x, y - 1)] == 'H':
                        edge.add((x, y - 1))

                    edge.add((x, y))
                    if coords[(x, y + 1)] == '~' or coords[(x, y + 1)] == 'H' or coords[(x, y + 1)] == '☼':
                        self.verticals.append(Vertical(edge.copy(), digging_zones.copy(), (x, y)))
                        edge.clear()
                        digging_zones.clear()
                        continue

                    if coords[(x, y + 1)] == '#':
                        if len(edge) > 1:
                            self.verticals.append(Vertical(edge.copy(), digging_zones.copy(), (x, y)))
                            edge.clear()
                            digging_zones.clear()
                            edge.add((x, y))
                            continue

                        if len(edge) == 1:
                            if coords[(x, y + 2)] == ' ':
                                edge.add((x, y + 1))
                                digging_zones.add((x, y + 1))
                                y += 1
                                continue

                if coords[(x, y)] == '☼':
                    if len(edge) > 0:
                        self.verticals.append(Vertical(edge.copy(), digging_zones.copy()))
                        edge.clear()
                        digging_zones.clear()
                    continue

                if coords[(x, y)] == '#':
                    if len(edge) > 0:
                        edge.add((x, y))
                        digging_zones.add((x, y))
                        if coords[(x, y + 1)] == ' ':
                            continue
                        if coords[(x, y + 1)] == '~':
                            edge.add((x, y + 1))
                            self.verticals.append(Vertical(edge.copy(), digging_zones.copy(), (x, y + 1)))
                            edge.clear()
                            digging_zones.clear()
                            continue
                        self.verticals.append(Vertical(edge.copy(), digging_zones.copy(), (x, y)))
                        edge.clear()
                        digging_zones.clear()

                    continue

                if coords[(x, y)] == '~':
                    if len(edge) == 0:
                        if coords[(x, y - 1)] == ' ':
                            edge.add((x, y))
                            edge.add((x, y - 1))
                        else:
                            if coords[(x, y + 1)] == ' ':
                                edge.add((x, y))

    def _set_intersecting_points_for_horizontals(self) -> None:
        for h_index, horizontal in enumerate(self.horizontals):
            for v_index, vertical in enumerate(self.verticals):
                if vertical.end_point is not None:  # if not ladder
                    if vertical.end_point in horizontal.points:
                        self.horizontals[h_index].intersecting_points.append((v_index, vertical.end_point))
                else:
                    if not horizontal.points.isdisjoint(vertical.points):
                        for p in horizontal.points.intersection(vertical.points):
                            self.horizontals[h_index].intersecting_points.append((v_index, p))

    def _set_intersecting_points_for_verticals(self) -> None:
        for v_index, vertical in enumerate(self.verticals):
            for h_index, horizontal in enumerate(self.horizontals):
                if not vertical.points.isdisjoint(horizontal.points):
                    for p in vertical.points.intersection(horizontal.points):
                        self.verticals[v_index].intersecting_points.append((h_index, p))

    def _get_vertical_with_specific_bag(self, bag_coord: (int, int)) -> int:
        for i, v in enumerate(self.verticals):
            if bag_coord in v.bags_points:
                return i

    def _get_all_allowed_bags(self, bags: list[(int, int)]) -> list[(int, (int, int))]:
        allowed_bags_list = list()  # single element = (distance, (x-coord, y-coord))
        for bag in bags:
            distance = self._validating_single_bag(bag)
            if distance != -1:
                allowed_bags_list.append((distance, bag))
        return allowed_bags_list

    # TODO: add formula to calculate this
    def _chose_best_bag_from_allowed(self, bags: list[(int, (int, int))]) -> (int, int):
        bags.sort(key=lambda x: x[0])
        return bags[0]

    def _get_distances_to_adjacent_edges(self, points_of_intersecting_with_adjacent_edges: list[(int, (int, int))],
                                         current_coordinates: (int, int), coordinate_axis: int,
                                         base_distance=0, is_first_iter=False, reverse=True,
                                         start_edge_index=None) -> list[tuple, int]:
        coordinates_with_distances = list()

        if is_first_iter and coordinate_axis == 1:
            for p in points_of_intersecting_with_adjacent_edges:
                dist = current_coordinates[coordinate_axis] - p[1][coordinate_axis]
                if dist >= 0:
                    coordinates_with_distances.append((p, dist + base_distance))
        else:
            for p in points_of_intersecting_with_adjacent_edges:
                coordinates_with_distances.append((p, abs(current_coordinates[coordinate_axis] - p[1][coordinate_axis])
                                                   + base_distance))

        if start_edge_index is not None:
            for c in self.verticals[start_edge_index].digging_zones:
                for i, p in enumerate(coordinates_with_distances):
                    if ((current_coordinates[1] >= c[1] >= p[0][1][1]) or
                            (current_coordinates[1] <= c[1] <= p[0][1][1])):
                        lst = list(coordinates_with_distances[i])
                        lst[1] += 1
                        coordinates_with_distances[i] = lst

        coordinates_with_distances.sort(key=lambda x: x[1], reverse=reverse)
        return coordinates_with_distances

    def _get_best_way_to_bag(self, bag: (int, (int, int))) -> list[(int, int)]:
        queue = list()  # for child - ((index, (x, y)), distance)
        used: list[int] = []
        last_item: int = -1

        vertical = self._get_vertical_with_specific_bag(bag[1])
        used.append(vertical)

        ways = self._get_distances_to_adjacent_edges(
            self.verticals[vertical].intersecting_points,
            bag[1],
            1,
            is_first_iter=True,
            start_edge_index=vertical,
            reverse=False
        )
        for w in ways:
            queue.append((w, 0))

        prev_iter_count = 0
        iter_count = len(queue)
        q_iter = iter(queue)
        q_index = 0
        not_first_step = False

        for q in q_iter:

            if not_first_step:
                prev_iter_count = iter_count
                iter_count = len(queue)
            else:
                not_first_step = True
            counter = iter_count - prev_iter_count
            while counter != 0:
                q_index += 1
                counter -= 1
                index = q[0][0][0]
                if -index in used:
                    try:
                        q = next(q_iter)
                    except StopIteration:
                        pass
                    continue
                used.append(-index)

                coord = q[0][0][1]
                base_distance = q[0][1]
                if base_distance > bag[0]:
                    try:
                        q = next(q_iter)
                    except StopIteration:
                        pass
                    continue
                if self.horizontals[index].has_hero:
                    last_item = q_index - 1
                    try:
                        q = next(q_iter)
                    except StopIteration:
                        pass
                    continue

                ways = self._get_distances_to_adjacent_edges(
                    self.horizontals[index].intersecting_points,
                    coord,
                    0,
                    base_distance,
                    reverse=False
                )
                for w in ways:
                    queue.append((w, q_index - 1))

                try:
                    q = next(q_iter)
                except StopIteration:
                    pass

            prev_iter_count = iter_count
            iter_count = len(queue)
            counter = iter_count - prev_iter_count

            while counter != 0:
                counter -= 1
                q_index += 1
                index = q[0][0][0]
                if index in used:
                    if counter != 0:
                        q = next(q_iter)
                    continue
                used.append(index)

                coord = q[0][0][1]
                base_distance = q[0][1]

                ways = self._get_distances_to_adjacent_edges(
                    self.verticals[index].intersecting_points,
                    coord,
                    1,
                    base_distance,
                    start_edge_index=index,
                    reverse=False
                )
                for w in ways:
                    queue.append((w, q_index - 1))

                if counter != 0:
                    q = next(q_iter)

        steps = []
        if last_item == -1:
            raise IndexError

        next_step = last_item
        steps.append(queue[next_step][0][0][1])
        not_first_iter = False
        while True:
            if next_step != 0:
                if not_first_iter:
                    steps.append(queue[next_step][0][0][1])
                else:
                    not_first_iter = True
                next_step = queue[next_step][1]
            else:
                steps.append(bag[1])
                break
        return steps

    def _validating_single_bag(self, bag: (int, int)) -> int:
        distance_to_nearest_enemy = 9999
        distance_to_hero = None

        vertical_queue = deque()  # for child - ((int, (int, int)), int)
        horizontal_queue = deque()  # for child - ((index, (x, y)), distance)
        vertical_used: set[int] = set()
        horizontal_used: set[int] = set()

        vertical = self._get_vertical_with_specific_bag(bag)  # id
        vertical_used.add(vertical)

        ways = self._get_distances_to_adjacent_edges(self.verticals[vertical].intersecting_points,
                                                     bag, 1, is_first_iter=True, start_edge_index=vertical)
        for w in ways:
            horizontal_queue.append(w)

        while horizontal_queue:

            while horizontal_queue:
                index = horizontal_queue[-1][0][0]
                if index in horizontal_used:
                    horizontal_queue.pop()
                    continue
                horizontal_used.add(index)

                coord = horizontal_queue[-1][0][1]
                base_distance = horizontal_queue[-1][1]

                if distance_to_hero:
                    if base_distance >= distance_to_hero:
                        horizontal_queue.pop()
                        continue
                if base_distance >= distance_to_nearest_enemy:
                    horizontal_queue.pop()
                    continue

                if self.horizontals[index].has_enemies:
                    is_needed_break = False
                    distance_to_hero = (
                        abs(self.horizontals[index].hero_x_coord - coord[0]) +
                        base_distance +
                        self.horizontals[index].hero_y_offset)
                    for i, c in enumerate(self.horizontals[index].enemies_x_coord):
                        distance = abs(c - coord[0]) + base_distance + self.horizontals[index].enemies_y_offset[i]
                        if distance < distance_to_nearest_enemy:
                            distance_to_nearest_enemy = distance
                            if distance_to_hero is not None:
                                if distance_to_nearest_enemy <= distance_to_hero:
                                    horizontal_queue.clear()
                                    is_needed_break = True
                                    break
                    if is_needed_break:
                        break

                if self.horizontals[index].has_hero:
                    distance_to_hero = (
                            abs(self.horizontals[index].hero_x_coord - coord[0]) +
                            base_distance +
                            self.horizontals[index].hero_y_offset)
                    if distance_to_hero >= distance_to_nearest_enemy:
                        horizontal_queue.clear()
                        break

                ways = self._get_distances_to_adjacent_edges(
                    self.horizontals[horizontal_queue.pop()[0][0]].intersecting_points,
                    coord,
                    0,
                    base_distance
                )
                for w in ways:
                    vertical_queue.append(w)

            else:
                while vertical_queue:
                    index = vertical_queue[-1][0][0]
                    if index in vertical_used:
                        vertical_queue.pop()
                        continue
                    vertical_used.add(index)

                    coord = vertical_queue[-1][0][1]
                    base_distance = vertical_queue[-1][1]

                    ways = self._get_distances_to_adjacent_edges(
                        self.verticals[vertical_queue.pop()[0][0]].intersecting_points,
                        coord,
                        1,
                        base_distance,
                        start_edge_index=index
                    )
                    for w in ways:
                        horizontal_queue.append(w)

        if distance_to_hero is not None and distance_to_hero < distance_to_nearest_enemy:
            return distance_to_hero
        return -1

    def clear(self) -> None:
        for i, h in enumerate(self.horizontals):
            if h.has_hero:
                self.horizontals[i].has_hero = False
                self.horizontals[i].hero_x_coord = None
                self.horizontals[i].hero_y_offset = None
            if h.has_enemies:
                self.horizontals[i].has_enemies = False
                self.horizontals[i].enemies_x_coord = None
                self.horizontals[i].enemies_y_offset = None

        for i, v in enumerate(self.verticals):
            self.verticals[i].bags_points = list()

    def set_hero_position(self, coords: (int, int)) -> None:
        for index, horizontal in enumerate(self.horizontals):
            if coords in horizontal.points:
                self.horizontals[index].has_hero = True
                self.horizontals[index].hero_x_coord = coords[0]
                self.horizontals[index].hero_y_offset = 0
                break
        else:
            offset = 0
            while True:
                is_needed_break = False
                lst = list(coords)
                offset += 1
                lst[1] += offset
                for index, horizontal in enumerate(self.horizontals):
                    if tuple(lst) in horizontal.points:
                        self.horizontals[index].has_hero = True
                        self.horizontals[index].hero_x_coord = coords[0]
                        self.horizontals[index].hero_y_offset = offset

                        is_needed_break = True
                        break
                if is_needed_break:
                    break

    def set_enemies_positions(self, coords: list[(int, int)]) -> None:
        for coord in coords:
            for index, horizontal in enumerate(self.horizontals):
                if coord in horizontal.points:
                    if not self.horizontals[index].has_enemies:
                        self.horizontals[index].has_enemies = True
                        self.horizontals[index].enemies_x_coord = list()
                        self.horizontals[index].enemies_y_offset = list()

                    self.horizontals[index].enemies_x_coord.append(coord[0])
                    self.horizontals[index].enemies_y_offset.append(0)
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
                            if not self.horizontals[index].has_enemies:
                                self.horizontals[index].has_enemies = True
                                self.horizontals[index].enemies_x_coord = list()
                                self.horizontals[index].enemies_y_offset = list()

                            self.horizontals[index].enemies_x_coord.append(coord[0])
                            self.horizontals[index].enemies_y_offset.append(offset)

                            is_needed_break = True
                            break
                    if is_needed_break:
                        break

    def set_bags_positions(self, bags: list[(int, int)]) -> None:
        for bag in bags:
            for i, v in enumerate(self.verticals):
                if bag in v.points:
                    self.verticals[i].bags_points.append(bag)

    def get_next_step_coordinates(self, bags: list[(int, int)]) -> list[(int, int)]:
        bag = self._chose_best_bag_from_allowed(self._get_all_allowed_bags(bags))
        return self._get_best_way_to_bag(bag)
