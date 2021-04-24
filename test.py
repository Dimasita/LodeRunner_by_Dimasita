from map import Map

maps = []


def check_map(map_str: str) -> None:
    cur_map = Map()
    cur_map.set_base_map_string(map_str)
    if cur_map.is_hero_alive():
        maps.append(cur_map)

