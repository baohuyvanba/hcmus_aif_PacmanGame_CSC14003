import math
import random

class GameState:
    def __init__(self, pacman_pos, foods_pos, monsters_pos, points,time_visits, pre_pos):
        self.pacman_pos = pacman_pos
        self.foods_pos = foods_pos
        self.monsters_pos = monsters_pos
        self.points = points
        self.time_visits = time_visits
        self.pre_pos = pre_pos

    def get_monster_move(self, graph_map):
        new_monsters_pos = []
        # Directions (left, up, right, down)
        directions = [(0, -1), (-1, 0), (0, 1), (1, 0)]
        k = [0, 1, 2, 3]
        random_list = []
        for i in k:
            random_list.insert(random.randint(0, len(k) - 1), i)
        for pos in self.monsters_pos:
            for direction in random_list:
                new_pos = (pos[0] + directions[direction][0], pos[1] + directions[direction][1])
                if is_valid_pos(graph_map, new_pos):
                    new_monsters_pos.append((pos[0] + directions[direction][0], pos[1] + directions[direction][1]))
                    break
        return new_monsters_pos
    def get_extension(self, graph_map):
        directions = [(0, -1), (-1, 0), (0, 1), (1, 0)]
        for direction in directions:
            new_pos = (self.pacman_pos[0] + direction[0], self.pacman_pos[1] + direction[1])
            if is_valid_pos(graph_map,new_pos):
                self.points += 1

def heuristic(state, goal):  # Diagonal
    # dx = abs(state[0] - goal[0])
    # dy = abs(state[1] - goal[1])
    # return dx + dy - min(dx, dy)
    return math.sqrt(abs(state[0] - goal[0]) ** 2 + abs(state[1] - goal[1]) ** 2)

# Function for level4 (Minimax or something like this)
def evaluation_function(graph_map, game_state):
    if game_state.pacman_pos in game_state.monsters_pos:
        game_state.points -= 500
    game_state.get_extension(graph_map)
    return game_state.points


def is_terminal_state(graph_map, game_state):
    return game_state.pacman_pos in game_state.monsters_pos


def is_valid_pos(graph_map, pos):
    return pos in graph_map

def get_moves(graph_map, game_state, player):
    '''
    input: graph map, gamestate, player (monster or pacman)
    output:
    4 (if possible) states for pacman
    or a state next move of monster (using A*)
    '''
    pacman_pos = game_state.pacman_pos
    foods_pos = game_state.foods_pos
    monsters_pos = game_state.monsters_pos
    points = game_state.points
    time_visits = game_state.time_visits
    pre_pos = game_state.pre_pos
    possible_moves = []
    if player:  # pacman
        # Directions (left, up, right, down)
        directions = [(0, -1), (-1, 0), (0, 1), (1, 0)]

        for direction in directions:
            new_pacman_pos = (pacman_pos[0] + direction[0], pacman_pos[1] + direction[1])
            if is_valid_pos(graph_map, new_pacman_pos) and new_pacman_pos not in monsters_pos:
                new_points = points
                if new_pacman_pos in foods_pos:
                    new_points += 20
                else:
                    new_points -= 1
                if new_pacman_pos == pre_pos:
                    new_points -=10
                new_points -= time_visits[new_pacman_pos]
                new_foods_pos = [pos for pos in foods_pos if pos != new_pacman_pos]
                new_game_state = GameState(new_pacman_pos, new_foods_pos, monsters_pos, new_points,time_visits,pre_pos)
                possible_moves.append(new_game_state)
        return possible_moves
    else:  # Monster
        new_monsters_pos = []
        # Directions (left, up, right, down)
        directions = [(0, -1), (-1, 0), (0, 1), (1, 0)]
        for pos in monsters_pos:
            temp = []
            for direction in directions:
                new_pos = (pos[0] + direction[0], pos[1] + direction[1])
                if is_valid_pos(graph_map, new_pos):
                    temp.append(heuristic(pacman_pos, new_pos))
                else:
                    temp.append(float('inf'))
            index_min = temp.index(min(temp))
            new_monsters_pos.append((pos[0] + directions[index_min][0], pos[1] + directions[index_min][1]))
        new_game_state = GameState(pacman_pos, foods_pos, new_monsters_pos, points,time_visits, pre_pos)
        # possible_moves.append(new_game_state)
        return new_game_state


def alpha_beta(graph_map, game_state, depth, player, alpha, beta):
    if depth == 0 or (is_terminal_state(graph_map, game_state)):
        return evaluation_function(graph_map, game_state), None

    if player:  # Pacman
        max_eval = float('-inf')
        best_move = None
        list_states = get_moves(graph_map, game_state, True)
        if list_states == []:
            return evaluation_function(graph_map, game_state), None
        for sub_state in list_states:

            eval, temp = alpha_beta(graph_map, sub_state, depth - 1, False, alpha, beta)
            if eval > max_eval:
                max_eval = eval
                best_move = sub_state.pacman_pos
            alpha = max(alpha, max_eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None
        list_states = get_moves(graph_map, game_state, False)
        # for sub_state in list_states:
        eval, temp = alpha_beta(graph_map, list_states, depth - 1, True, alpha, beta)
        if eval < min_eval:
            min_eval = eval
            best_move = list_states.monsters_pos
        beta = min(beta, min_eval)
        return min_eval, best_move