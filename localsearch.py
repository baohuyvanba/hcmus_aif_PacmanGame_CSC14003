def heuristic_lv3_around(graph_map, position, foods_pos, pre_pos, monster_pos):
    heu = 0
    if position in foods_pos:
        heu += 2
    if position in monster_pos:
        heu -= 25
    for pos in graph_map[position]:
        if pos in pre_pos:
            continue
        if pos in foods_pos and pos not in pre_pos:
            pre_pos.append(pos)
            heu += 2
        elif pos in monster_pos:
            heu -= 15

    return heu


def heuristic_lv3_2around(pacman_pos, graph_map, position, foods_pos, monster_pos):
    heu = 0
    if position in foods_pos:
        heu += 2
    if position in monster_pos:
        heu -= 35
    pre_pos = []
    pre_pos.append(position)
    pre_pos.append(pacman_pos)
    for pos in graph_map[position]:
        if pos == pacman_pos:
            continue
        heu = heu + heuristic_lv3_around(graph_map, pos, foods_pos, pre_pos, monster_pos)
    return heu