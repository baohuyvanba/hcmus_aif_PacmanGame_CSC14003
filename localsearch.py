#Heuristic Local Search
from constant_value import *

class Cell:
    def __init__(self, position, state):
        self.position = position
        self.state    = state    #List of state: Blank = pathway, s_state_food, s_state_monster, s_state_pacman
        self.heuristic = 0
        self.visited = 0

    #Check if cell contains Food
    def food_here(self):
        return (s_state_food in self.state)

    #Check if cell contains Monster
    def monster_here(self):
        return (s_state_monster in self.state)

    # Check if cell contains Monster
    def monster_here(self):
        return (s_state_monster in self.state)

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

    def reset_heuristic(self):
        self.heuristic = 0

    def objective_function(self):
        return self.heuristic - self.visited

#######################################################################################################################
def calc_heuristic(cells, graph_map, remembered, start, cur, max_depth):
    remembered.append(cur.position)

    if max_depth <= 0:
        return

    for child in graph_map[cur]:
        if child.position not in remembered:

            sub_remembered = []
            if child.food_here():
                update_heuristic(cells, graph_map, sub_remembered, start, child, 2, "food")

            sub_remembered = []
            if child.monster_here():
                update_heuristic(cells, graph_map, sub_remembered, start, child, 2, "monster")

            calc_heuristic(cells, graph_map, remembered.copy(), start, child, max_depth - 1)

    cur.heuristic -= cur.visited


def clear_heuristic(cells, graph_map, remembered, cur, max_depth):
    remembered.append(cur.position)

    if max_depth <= 0:
        return

    for child in graph_map[cur]:
        if child.position not in remembered:
            child.reset_heuristic()

            clear_heuristic(cells, graph_map, remembered.copy(), child, max_depth - 1)


def update_heuristic(cells, graph_map, remembered, start, cur, max_depth, cell_type):
    remembered.append(cur.position)

    if max_depth < 0:
        return

    if cur.position == start.position:
        return

    if cell_type == "food":
        food = 0
        if max_depth == 2: food = 35
        if max_depth == 1: food = 10
        if max_depth == 0: food = 5
        cur.heuristic += food

    if cell_type == "monster":
        monster = 0
        if max_depth == 2: monster = float("-inf")
        if max_depth == 1: monster = float("-inf")
        if max_depth == 0: monster = -100
        cur.heuristic += monster

    for child in graph_map[cur]:
        if child.position not in remembered:
            update_heuristic(cells, graph_map, remembered.copy(), start, child, max_depth - 1, cell_type)


def local_search(cells, graph_map, pacman_position):
    remembered = []
    clear_heuristic(cells, graph_map, remembered, pacman_position, 3)

    remembered = []
    calc_heuristic(cells, graph_map, remembered, pacman_position, pacman_position, 3)

    max_f = float("-inf")
    next_step = None

    for child in graph_map[pacman_position]:
        if max_f < child.objective_function():
            max_f = child.objective_function()
            next_step = child

    return next_step


