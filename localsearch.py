#Heuristic Local Search
from constant_value import *

class Cell:
    def __init__(self, position, state):
        self.position = position   #Cell position in O_x_y Co-ordinate
        self.state    = state      #List of state: Blank = pathway, s_state_food, s_state_monster, s_state_pacman
        self.heuristic = 0
        self.visited = 0

    #Check if cell contains Food
    def food_here(self):
        return (s_state_food in self.state)

    #Check if cell contains Monster
    def monster_here(self):
        return (s_state_monster in self.state)

    # Check if cell contains Monster
    # def monster_here(self):
    #     return (s_state_monster in self.state)

    #Food is eaten by Pacman
    def food_eaten(self):
        self.state.remove(s_state_food)

    #Monster goes in
    def in_monster(self):
        self.state.append(s_state_monster)

    #Monster goes out
    def out_monster(self):
        self.state.remove(s_state_monster)

    #Pacman goes in and eats food (if present)
    def in_pacman(self):
        self.state.append(s_state_pacman)
        if self.food_here():
            self.food_eaten()
        self.visited += 1

    #Pacman goes out
    def out_pacman(self):
        self.state.remove(s_state_pacman)

    #Reset cell's heuristic value to 0
    def reset_heuristic(self):
        self.heuristic = 0

    #Return priority value
    def objective_function(self):
        return self.heuristic - self.visited


# HEURISTIC LOCAL SEARCH FUNCTIONS #####################################################################################
def cal_heurictis_value(cells, map_graph, center_position, visibility_cell):
    #center_position is the position of pacman.
    #visibility_cell is list of cells in pacman's visibility area
    pacman_pos = center_position
    visited = [center_position]
    #
    #radius = 1
    for neighbor_1 in map_graph[pacman_pos]:
        visited.append(neighbor_1)
        #
        if neighbor_1.food_here():          #Cell contain food, add heuristic value to surround cell (radius = 3)
            re_calculate_heuristic(cells, map_graph, center_position, neighbor_1, visibility_cell, s_state_food)
        if neighbor_1.monster_here():       #Cell contain monster, add heuristic value to surround cell (radius = 3)
            re_calculate_heuristic(cells, map_graph, center_position, neighbor_1, visibility_cell, s_state_monster)

    #radius = 2
    for n1 in visited[1:]:
        for neighbor_2 in map_graph[n1]:
            if neighbor_2 not in visited:
                visited.append(neighbor_2)
                #
                if neighbor_2.food_here():  # Cell contain food, add heuristic value to surround cell (radius = 3)
                    re_calculate_heuristic(cells, map_graph, center_position, neighbor_2, visibility_cell, s_state_food)
                if neighbor_2.monster_here():  # Cell contain monster, add heuristic value to surround cell (radius = 3)
                    re_calculate_heuristic(cells, map_graph, center_position, neighbor_2, visibility_cell, s_state_monster)

    #radius = 3
    for n2 in visited[5:]:
        for neighbor_3 in map_graph[n2]:
            if neighbor_3 not in visited:
                visited.append(neighbor_3)
                #
                if neighbor_3.food_here():  # Cell contain food, add heuristic value to surround cell (radius = 3)
                    re_calculate_heuristic(cells, map_graph, center_position, neighbor_3, visibility_cell, s_state_food)
                if neighbor_3.monster_here():  # Cell contain monster, add heuristic value to surround cell (radius = 3)
                    re_calculate_heuristic(cells, map_graph, center_position, neighbor_3, visibility_cell, s_state_monster)


#Backup
# def calc_heuristic(cells, graph_map, remembered, start, cur, max_depth):
#     remembered.append(cur.position)
#     if max_depth <= 0:
#         return
#     for child in graph_map[cur]:
#         if child.position not in remembered:
#             sub_remembered = []
#             if child.food_here():
#                 update_heuristic(cells, graph_map, sub_remembered, start, child, 2, "food")
#             sub_remembered = []
#             if child.monster_here():
#                 update_heuristic(cells, graph_map, sub_remembered, start, child, 2, "monster")
#
#             calc_heuristic(cells, graph_map, remembered.copy(), start, child, max_depth - 1)
#     cur.heuristic -= cur.visited


def re_calculate_heuristic(cells, map_graph, center_position, current_cell, visibility_cell, s_state):
    # center_position is the position of pacman.
    # visibility_cell is list of cells in pacman's visibility area
    visited = [current_cell]
    # radius = 1
    cell_in_rad_1 = 0
    for neighbor_1 in map_graph[current_cell]:
        if neighbor_1 in visibility_cell and neighbor_1 != center_position:
            cell_in_rad_1 += 1
            visited.append(neighbor_1)
            #
            if s_state == s_state_food:
                if neighbor_1.food_here():    # Cell in radius 1 contain food
                    current_cell.heuristic += s_food_1
            if s_state == s_state_monster:
                if neighbor_1.monster_here(): # Cell in radius 1 contain monster
                    current_cell.heuristic += s_mons_1

    # radius = 2
    for n1 in visited[1:]:
        # if n1 not in visibility_cell:
        #     continue
        for neighbor_2 in map_graph[n1]:
            #if neighbor_2 in visibility_cell and neighbor_2 not in visited and neighbor_2 != center_position:
            if neighbor_2 in visibility_cell and neighbor_2 != center_position:
                visited.append(neighbor_2)
                #
                if s_state == s_state_food:
                    if neighbor_2.food_here():     # Cell in radius 2 contain food
                        current_cell.heuristic += s_food_2
                if s_state == s_state_monster:
                    if neighbor_2.monster_here():  # Cell in radius 2 contain monster
                        current_cell.heuristic += s_mons_2

    #radius = 3
    for n2 in visited[(1+cell_in_rad_1):]:
        #if n2 not in visibility_cell:
        #     continue
        for neighbor_3 in map_graph[n2]:
            #if neighbor_3 in visibility_cell and neighbor_3 not in visited and neighbor_3 != center_position:
            if neighbor_3 in visibility_cell and neighbor_3 != center_position:
                visited.append(neighbor_3)
                #
                if s_state == s_state_food:
                    if neighbor_3.food_here():          # Cell in radius 3 contain food
                        current_cell.heuristic += s_food_3
                if s_state == s_state_monster:
                    if neighbor_3.monster_here():       # Cell in radius 3 contain monster
                        current_cell.heuristic += s_mons_3


#Backup
# def update_heuristic(cells, graph_map, remembered, start, cur, max_depth, cell_type):
#     remembered.append(cur.position)
#     if max_depth < 0:
#         return
#     if cur.position == start.position:
#         return
#     if cell_type == "food":
#         food = 0
#         if max_depth == 2: food = 35
#         if max_depth == 1: food = 10
#         if max_depth == 0: food = 5
#         cur.heuristic += food
#     if cell_type == "monster":
#         monster = 0
#         if max_depth == 2: monster = float("-inf")
#         if max_depth == 1: monster = float("-inf")
#         if max_depth == 0: monster = -100
#         cur.heuristic += monster
#     for child in graph_map[cur]:
#         if child.position not in remembered:
#             update_heuristic(cells, graph_map, remembered.copy(), start, child, max_depth - 1, cell_type)


def reset_visibility_heuristic(cells, map_graph, pacman_pos):
    visited = [pacman_pos]
    for neighbor_1 in map_graph[pacman_pos]:
        visited.append(neighbor_1)
        neighbor_1.reset_heuristic()

    for n1 in visited[1:]:
        for neighbor_2 in map_graph[n1]:
            if neighbor_2 not in visited:
                visited.append(neighbor_2)
                neighbor_2.reset_heuristic()

    for n2 in visited[5:]:
        for neighbor_3 in map_graph[n2]:
            if neighbor_3 not in visited:
                visited.append(neighbor_3)
                neighbor_3.reset_heuristic()
    return visited


#Backup
# def clear_heuristic(cells, graph_map, remembered, cur, max_depth):
#     remembered.append(cur.position)
#     if max_depth <= 0:
#         return
#     for child in graph_map[cur]:
#         if child.position not in remembered:
#             child.reset_heuristic()
#             clear_heuristic(cells, graph_map, remembered.copy(), child, max_depth - 1)


def local_search(cells, graph_map, pacman_pos):                                     #Local Search: the bigger Heuristic value is, the higher priority of next step is: Input(cell matrix, map_graph, pacman_pos)
    visibility_cell = reset_visibility_heuristic(cells, graph_map, pacman_pos)

    cal_heurictis_value(cells, graph_map, pacman_pos, visibility_cell)

    max_f = float("-inf")
    next_step = None

    for child in graph_map[pacman_pos]:
        if max_f < child.objective_function():
            max_f = child.objective_function()
            next_step = child

    return next_step


