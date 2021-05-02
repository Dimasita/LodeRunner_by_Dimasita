from decorators import benchmark
from collections import deque
from graph import Edge
from board import Board


edges = Edge()
board = Board('123')



def create_list_of_horizontals(coords: dict[[int, int], str]) -> None:
    edge = set()    # to save coordinates of one edge of a graph

    real_board_side_length = board.map_side_length - 1
    for y in range(board.map_side_length):
        for x in range(real_board_side_length):

            if coords[(x, y)] == '#' or coords[(x, y)] == '☼':
                if len(edge) > 0:
                    edges.add_horizontal(edge.copy())
                    edge.clear()
                else:
                    if coords[(x, y)] == '#' and (coords[(x, y + 1)] == '#' or coords[(x, y + 1)] == '☼') and \
                            (coords[(x, y - 1)] == '#' or coords[(x, y - 1)] == '☼'):
                        edges.add_horizontal(edge.copy())
                        edge.clear()
                continue

            if coords[(x, y + 1)] != ' ' or coords[(x, y)] == 'H' or coords[(x, y)] == '~':
                edge.add((x, y))
                continue

            if len(edge) > 0:
                edge.add((x, y))
                edges.add_horizontal(edge.copy())
                edge.clear()

            if coords[(x + 1, y)] != '#' and coords[(x + 1, y)] != '☼' and \
                    (coords[(x + 1, y + 1)] != ' ' or
                     (coords[(x + 1, y)] == 'H' or coords[(x + 1, y)] == '~')):
                edge.add((x, y))
                x += 1
                edge.add((x, y))


def create_list_of_verticals(coords: dict[[int, int], str]) -> None:
    edge = set()
    digging_zones = set()
    for x in range(board.map_side_length):
        for y in range(board.map_side_length):

            if coords[(x, y)] == 'H':
                if coords[(x, y - 1)] == ' ' or coords[(x, y - 1)] == '~':
                    edge.add((x, y - 1))

                edge.add((x, y))
                if coords[(x, y + 1)] != 'H':
                    edges.add_vertical(edge.copy(), digging_zones.copy())
                    edge.clear()
                    digging_zones.clear()
                continue

            if coords[(x, y)] == ' ':
                if coords[(x, y - 1)] == 'H':
                    edge.add((x, y - 1))

                edge.add((x, y))
                if coords[(x, y + 1)] == '~' or coords[(x, y + 1)] == 'H' or coords[(x, y + 1)] == '☼':
                    edges.add_vertical(edge.copy(), digging_zones.copy(), (x, y))
                    edge.clear()
                    digging_zones.clear()

                    continue
                if coords[(x, y + 1)] == '#':
                    if len(edge) > 1:
                        edges.add_vertical(edge.copy(), digging_zones.copy(), (x, y))
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
                    edges.add_vertical(edge.copy(), digging_zones.copy())
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
                        edges.add_vertical(edge.copy(), digging_zones.copy(), (x, y + 1))
                        edge.clear()
                        digging_zones.clear()
                        continue
                    edges.add_vertical(edge.copy(), digging_zones.copy(), (x, y))
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

    edges.set_intersecting_points_for_horizontal()


def get_vertical_with_specific_bag(bag_coord: tuple) -> int:
    for i, v in enumerate(edges.verticals):
        if bag_coord in v.bags_points:
            return i


def find_allowed_bag(bags: list[(int, int)]) -> list[(int, (int, int))]:
    list_of_dist = list()
    i = 0
    for bag in bags:
        i += 1
        dist = validating_single_bag(bag)
        if dist[0]:
            list_of_dist.append((dist, bag))
            print(f'К мешочку с координатами {bag} мы ближайшие!! '
                  f'Расстояние до нас - {dist[1]}, до челыбоса - {dist[2]}!')
        else:
            print(f'К мешочку с координатами {bag} мы дальше(( '
                  f'Расстояние до нас - {dist[1]}, до челыбоса - {dist[2]}!')

    list_of_dist.sort(key=lambda x: x[0])
    return list_of_dist


def validating_single_bag(bag_coord: (int, int)) -> (bool, int, int):
    distance_to_nearest_enemy = 9999
    distance_to_hero = None

    vertical_queue = deque()       # for child - tuple(tuple(int, tuple(int, int)), int)
    horizontal_queue = deque()     # for child - ((index, (x, y)), distance)
    vertical_used = set()          # int
    horizontal_used = set()        # int

    vertical = get_vertical_with_specific_bag(bag_coord)   # id
    vertical_used.add(vertical)

    ways = sort_ways_by_distance_desc(edges.verticals[vertical].intersecting_points,
                                      bag_coord, 1, is_first_iter=True, start_edge_index=vertical)
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

            if edges.horizontals[index].has_enemies:
                is_needed_break = False
                for c in edges.horizontals[index].enemies_coords:
                    # if enemy in flight (first char-numbers of digits in offset, next-offset, next-coord)
                    if c < 0:
                        cnt = str(-c)
                        chars = ''
                        for ch in range(1, int(cnt[0]) + 1):
                            chars += str(ch)
                        offset = int(chars)
                        chars = ''
                        for ch in range(int(cnt[0]) + 1, len(cnt)):
                            chars += str(ch)
                        x_coord = int(chars)
                        d = abs(x_coord - coord[0]) + base_distance + offset
                    else:
                        d = abs(c - coord[0]) + base_distance
                    if d < distance_to_nearest_enemy:
                        distance_to_nearest_enemy = d
                        if distance_to_hero:
                            if distance_to_nearest_enemy <= distance_to_hero:
                                horizontal_queue.clear()
                                is_needed_break = True
                                break
                if is_needed_break:
                    break

            if edges.horizontals[index].has_hero:
                distance_to_hero = abs(edges.horizontals[index].hero_coords - coord[0]) \
                                   + base_distance + edges.horizontals[index].hero_offset
                if distance_to_hero >= distance_to_nearest_enemy:
                    horizontal_queue.clear()
                    break

            ways = sort_ways_by_distance_desc(edges.horizontals[horizontal_queue.pop()[0][0]].intersecting_points,
                                              coord, 0, base_distance)
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

                ways = sort_ways_by_distance_desc(edges.verticals[vertical_queue.pop()[0][0]].intersecting_points,
                                                  coord, 1, base_distance, start_edge_index=index)
                for w in ways:
                    horizontal_queue.append(w)

    if distance_to_hero:
        if distance_to_hero < distance_to_nearest_enemy:
            return True, distance_to_hero, distance_to_nearest_enemy
    if distance_to_hero is None:
        distance_to_hero = -1
    return False, distance_to_hero, distance_to_nearest_enemy


def sort_ways_by_distance_desc(ways: list, coord: (int, int), coord_index: int,
                               base_distance=None, is_first_iter=False,
                               start_edge_index=None) -> list[tuple, int]:
    distances_to_ways = list()

    for w in ways:
        distances_to_ways.append(coord[coord_index] - w[1][coord_index])

    if not is_first_iter:
        for i, d in enumerate(distances_to_ways):
            distances_to_ways[i] = abs(d) + base_distance
        sorted_ways = list(zip(ways, distances_to_ways))

    else:
        new_distances_to_ways = list(zip(ways, distances_to_ways))
        distances_to_ways.clear()
        for i in range(len(new_distances_to_ways)):
            if new_distances_to_ways[i][1] >= 0:
                distances_to_ways.append(new_distances_to_ways[i])
        sorted_ways = distances_to_ways

    if start_edge_index is not None:    # iteration by Y (verticals)
        if len(edges.verticals[start_edge_index].digging_zones) != 0:
            for c in edges.verticals[start_edge_index].digging_zones:
                for i, w in enumerate(sorted_ways):
                    if (coord[1] >= c[1] >= w[0][1][1]) or (coord[1] <= c[1] <= w[0][1][1]):
                        lst = list(sorted_ways[i])
                        lst[1] += 2
                        sorted_ways[i] = lst

    sorted_ways.sort(key=lambda x: x[1], reverse=True)
    return sorted_ways


def chose_best_bag_from_allowed(bags: list) -> list[(int, int)]:
    steps = []
    weights = []
    another_bags_count = []

    for b_ind, bag in enumerate(bags):
        weights.append(0)
        another_bags_count.append(0)

        queue = list()        # for child - ((index, (x, y)), distance)
        used = []             # int
        last_item = {}        # int

        vertical = get_vertical_with_specific_bag(bag[1])
        used.append(vertical)

        ways = sort_ways_by_distance_desc(edges.verticals[vertical].intersecting_points,
                                          bag[1], 1, is_first_iter=True, start_edge_index=vertical)
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
                if base_distance > bag[0][1]:
                    try:
                        q = next(q_iter)
                    except StopIteration:
                        pass
                    continue

                if edges.horizontals[index].has_hero:
                    weights[b_ind] = abs(edges.horizontals[index].hero_coords - coord[0]) \
                                       + base_distance + edges.horizontals[index].hero_offset
                    last_item[b_ind] = q_index - 1
                    try:
                        q = next(q_iter)
                    except StopIteration:
                        pass
                    continue

                ways = sort_ways_by_distance_desc(edges.horizontals[index].intersecting_points,
                                                  coord, 0, base_distance)
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
                        try:
                            q = next(q_iter)
                        except StopIteration:
                            pass
                    continue
                used.append(index)

                coord = q[0][0][1]
                base_distance = q[0][1]

                if len(edges.verticals[index].bags_points) > 0:
                    for b in edges.verticals[index].bags_points:
                        if b[1] < coord[1]:
                            another_bags_count[b_ind] += 1

                ways = sort_ways_by_distance_desc(edges.verticals[index].intersecting_points,
                                                  coord, 1, base_distance, start_edge_index=index)
                for w in ways:
                    queue.append((w, q_index - 1))

                if counter != 0:
                    q = next(q_iter)

        max_bags = 0

        indexes = []
        if len(weights) != 1:
            for i, e in enumerate(another_bags_count):
                if e > max_bags:
                    max_bags = e
                    indexes.clear()
                    indexes.append(i)
                else:
                    if max_bags != 0:
                        if e == max_bags:
                            indexes.append(i)

            main_index = -1
            min_weights = 1000
            for i in indexes:
                if weights[i] < min_weights:
                    min_weights = weights[i]
                    main_index = i

            if main_index == b_ind:
                steps.clear()
                next_step = last_item[b_ind]
                while True:
                    steps.append(queue[next_step][0][0][1])
                    if next_step != 0:
                        next_step = queue[next_step][1]
                    else:
                        break

        else:
            steps.clear()
            next_step = last_item[b_ind]
            while True:
                steps.append(queue[next_step][0][0][1])
                if next_step != 0:
                    next_step = queue[next_step][1]
                else:
                    steps.append(bag[1])
                    break
    return steps


def find_single_bag_way(bag: (int, int)) -> list[(int, int)]:
    weight = 0

    queue = list()        # for child - ((index, (x, y)), distance)
    used = []             # int
    last_item: int

    vertical = get_vertical_with_specific_bag(bag[1])
    used.append(vertical)

    ways = sort_ways_by_distance_desc(edges.verticals[vertical].intersecting_points,
                                      bag[1], 1, is_first_iter=True, start_edge_index=vertical)
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
            if base_distance > bag[0][1]:
                try:
                    q = next(q_iter)
                except StopIteration:
                    pass
                continue

            if edges.horizontals[index].has_hero:
                weight = abs(edges.horizontals[index].hero_coords - coord[0]) \
                                   + base_distance + edges.horizontals[index].hero_offset
                last_item = q_index - 1
                try:
                    q = next(q_iter)
                except StopIteration:
                    pass
                continue

            ways = sort_ways_by_distance_desc(edges.horizontals[index].intersecting_points,
                                              coord, 0, base_distance)
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

            ways = sort_ways_by_distance_desc(edges.verticals[index].intersecting_points,
                                              coord, 1, base_distance, start_edge_index=index)
            for w in ways:
                queue.append((w, q_index - 1))

            if counter != 0:
                q = next(q_iter)

    steps = []
    next_step = last_item
    while True:
        steps.append(queue[next_step][0][0][1])
        if next_step != 0:
            next_step = queue[next_step][1]
        else:
            steps.append(bag[1])
            break
    return steps


@benchmark(30)
def new_msg(base_map_string: str) -> str:

    on_start(base_map_string)

    list_of_bags = board.get_bags_positions()
    edges.set_bags_positions(list_of_bags)
    edges.set_enemies_positions(board.get_enemies_positions())

    hero_position = board.get_hero_position()
    edges.set_hero_position(hero_position)
    allowed_bags_distance = find_allowed_bag(list_of_bags)
    best_way = find_single_bag_way(allowed_bags_distance[0])
    # print(best_way, hero_position)
    action = 'stop'
    i = 0
    while True:
        if best_way[i][0] != hero_position[0]:
            move = best_way[i][0] - hero_position[0]
            if move > 0:
                action = 'right'
            else:
                action = 'left'
            if best_way[1][0] == hero_position[0] + 1:
                if (best_way[1][1] - hero_position[1]) > 0 and \
                        board.can_drill_block(hero_position[0] + 1, hero_position[1] + 1):
                    if action == 'left':
                        action = 'act,left'
                    else:
                        action = 'act,right'
            if best_way[1][0] == hero_position[0] - 1:
                if (best_way[1][1] - hero_position[1]) > 0 and \
                        board.can_drill_block(hero_position[0] - 1, hero_position[1] + 1):
                    if action == 'left':
                        action = 'act,left'
                    else:
                        action = 'act,right'
            break
        else:
            if best_way[i][1] != hero_position[1]:
                move = best_way[i][1] - hero_position[1]
                if move > 0:
                    if board.can_drill_block(hero_position[0], hero_position[1] + 1):
                        action = 'left'
                    else:
                        action = 'down'
                else:
                    action = 'up'
                break
            else:
                i += 1

    return action


def on_start(base_map_string: str):
    edges.empty()   # to pass in a loop (benchmark)
    board.set_base_map_string(base_map_string)
    coords = board.associate_map_with_coordinates()
    create_list_of_horizontals(coords)
    create_list_of_verticals(coords)
