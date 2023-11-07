def heuristic_lv3_around(graph_map,position,foods_pos,pre_pos,monster_pos):
    '''
    Input: graphmap, position (pacman), foods_pos (list of food pos[(),(),..]),prepos(position haved gone), 
    monster_pos (list of monster post) [(),(),..]
    Output: Giá trị heuristic
    Khi gặp monster cách pacman 2,3 bước đi thì giá trị sẽ lần lượt nhỏ hơn, -30, và -20
    '''
    heu = 0
    if position in foods_pos:
        heu+=2
    if position in monster_pos:
        heu -= 40
    for pos in graph_map[position]:
        if pos in pre_pos:
            continue
        if pos in foods_pos and pos not in pre_pos:
            pre_pos.append(pos)
            heu+=2
        elif pos in monster_pos:
            heu-=20

    return heu

def heuristic_lv3_2around(pacman_pos,graph_map,position,foods_pos,monster_pos):
    '''
    Input: pacman position, graphmap, postion: vị trí kế của pacman_pos đang xét (trái, trên, phải, dưới)
    foods_pos (list of food pos[(),(),..]),prepos(position haved gone), 
    monster_pos (list of monster post) [(),(),..]
    Output: Giá trị heuristic
    Check xem vị trí kế cận (1 bước đi) của pacman có phải là monster không, nếu có thì lấy 
    -60, sau đó từ vị trí này lại xét thêm 2 bước nữa (vì pacman nhận biết được 3 bước xung quanh)
    Nếu vị trí đó là.
    Tất nhiên là mình sẽ không xét lại vị trí trước đó (pacman_pos, đi tới vị trí này).
    '''
    heu = 0
    if position in foods_pos:
        heu+=2
    if position in monster_pos:
        heu -= 60
    pre_pos = []
    pre_pos.append(position)
    pre_pos.append(pacman_pos)
    for pos in graph_map[position]: 
        if pos == pacman_pos:
            continue
        heu = heu + heuristic_lv3_around(graph_map,pos,foods_pos,pre_pos,monster_pos)
    return heu     

# def heuristic_lv3_around(graph_map, position, foods_pos, pre_pos, monster_pos):
#     heu = 0
#     if position in foods_pos:
#         heu += 2
#     if position in monster_pos:
#         heu -= 25
#     for pos in graph_map[position]:
#         if pos in pre_pos:
#             continue
#         if pos in foods_pos and pos not in pre_pos:
#             pre_pos.append(pos)
#             heu += 2
#         elif pos in monster_pos:
#             heu -= 15

#     return heu


# def heuristic_lv3_2around(pacman_pos, graph_map, position, foods_pos, monster_pos):
#     heu = 0
#     if position in foods_pos:
#         heu += 2
#     if position in monster_pos:
#         heu -= 35
#     pre_pos = []
#     pre_pos.append(position)
#     pre_pos.append(pacman_pos)
#     for pos in graph_map[position]:
#         if pos == pacman_pos:
#             continue
#         heu = heu + heuristic_lv3_around(graph_map, pos, foods_pos, pre_pos, monster_pos)
#     return heu
