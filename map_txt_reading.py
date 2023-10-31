import localsearch as ls
from constant_value import *

def map_level1(path):
    file = open(path, "r")
    map_size = [int(val) for val in file.readline().split()]
    map_matrix = []
    for i in range(map_size[0]):
        map_matrix.append([int(val) for val in list(file.readline().split())])
    pacman_pos = [int(val) for val in list(file.readline().split())]
    food_pos = None

    #Declare graph map of pacman game
    map_graph = {}
        #row = y in co-ordinate
        #col = x in co-ordinate
    for row in range(len(map_matrix)):
        for col in range(len(map_matrix[row])):
            #Not a wall: path & food
            if map_matrix[row][col] != 1:
                #Food locator
                if map_matrix[row][col] == 2:
                    food_pos = (col, row)                                  #x = col, y = row theo từ ma trận -> trục tọa độ
                #Pathway
                current = (col, row)
                map_graph[current] = []                                #Danh sách ô liền kề với ô hiện tại (current cell)

                if col - 1 >= 0 and map_matrix[row][col - 1] != 1:         #Tồn tại ô bên trái + ô bên trái là pathway
                    left = (col - 1, row) #Vị trí ô bên trái
                    map_graph[left]    = map_graph[left] + [current]           #Thêm ô hiện tại vào danh sách kề ô bên trái
                    map_graph[current] = map_graph[current] + [left]           #Thêm ô bên trái vào danh sách kề ô hiện tại

                if row - 1 >= 0 and map_matrix[row - 1][col] != 1:         #Tồn tại ô bên trên + ô bên trên là pathway
                    up = (col, row - 1)  #Vị trí ô bên trên
                    map_graph[up]      = map_graph[up] + [current]             #Thêm ô hiện tại vào danh sách kề ô bên trên
                    map_graph[current] = map_graph[current] + [up]             #Thêm ô bên trên vào danh sách kề ô hiện tại

    return map_graph, (pacman_pos[0], pacman_pos[1]), food_pos

def map_level2(path, fakewall: bool):
    file = open(path, "r")
    map_size = [int(val) for val in file.readline().split()]
    map_matrix = []
    for i in range(map_size[0]):
        map_matrix.append([int(val) for val in list(file.readline().split())])
    pacman_pos = [int(val) for val in list(file.readline().split())]

    food_pos = None
    monsters_pos_list = []

    #Declare graph map of pacman game
    map_graph = {}
        #row = y in co-ordinate
        #col = x in co-ordinate
    for row in range(len(map_matrix)):
        for col in range(len(map_matrix[row])):
            if map_matrix[row][col] != 1:                                  #Monster
                # Food locator
                if map_matrix[row][col] == 2:
                    food_pos = (col, row)                                  #x = col, y = row theo từ ma trận -> trục tọa độ
                elif map_matrix[row][col] == 3:
                    monsters_pos_list.append((col, row))
                    # Monster is Wall
                    if fakewall:
                        map_matrix[row][col] = 1

                #Pathway
                current = (col, row)
                map_graph[current] = []                                    #Danh sách ô liền kề với ô hiện tại (current cell)

                if col - 1 >= 0 and map_matrix[row][col - 1] != 1:         #Tồn tại ô bên trái + ô bên trái là pathway
                    left = (col - 1, row) #Vị trí ô bên trái
                    map_graph[left]    = map_graph[left] + [current]       #Thêm ô hiện tại vào danh sách kề ô bên trái
                    map_graph[current] = map_graph[current] + [left]       #Thêm ô bên trái vào danh sách kề ô hiện tại

                if row - 1 >= 0 and map_matrix[row - 1][col] != 1:         #Tồn tại ô bên trên + ô bên trên là pathway
                    up = (col, row - 1)  #Vị trí ô bên trên
                    map_graph[up]      = map_graph[up] + [current]         #Thêm ô hiện tại vào danh sách kề ô bên trên
                    map_graph[current] = map_graph[current] + [up]         #Thêm ô bên trên vào danh sách kề ô hiện tại

    return map_graph, (pacman_pos[0], pacman_pos[1]), food_pos, monsters_pos_list

#Build Cell
def build_cell(matrix_map, pacman_pos):
    cells = []
        #y = row, x = col
    for row in range(len(matrix_map)):
        temp = []
        for col in range(len(matrix_map[row])):
            #Not wall
            if matrix_map[row][col] != 1:
                if matrix_map[row][col] == 0:
                    temp.append(ls.Cell((col, row), []))
                elif matrix_map[row][col] == 2:
                    temp.append(ls.Cell((col, row), [s_state_food]))
                elif matrix_map[row][col] == 3:
                    temp.append(ls.Cell((col, row), [s_state_monster]))

                if (col, row) == pacman_pos:
                    temp[col].state.append(s_state_pacman)
                    pacman_cell = temp[col]
            else:
                temp.append(None)
        cells.append(temp)

    return cells, pacman_cell


def map_level3(path):
    file = open(path, "r")
    map_size = [int(val) for val in file.readline().split()]
    map_matrix = []
    for i in range(map_size[0]):
        map_matrix.append([int(val) for val in list(file.readline().split())])
    pacman_pos_list = [int(val) for val in list(file.readline().split())]
    pacman_pos = (pacman_pos_list[0], pacman_pos_list[1])

    cells, pacman_cell = build_cell(map_matrix, pacman_pos)

    food_cell_list = []
    monsters_cell_list = []
    map_graph = {}
        # row = y in co-ordinate
        # col = x in co-ordinate
    for row in range(len(map_matrix)):
        for col in range(len(map_matrix[row])):
            if map_matrix[row][col] != 1:
                #Food
                if s_state_food in cells[row][col].state:
                    food_cell_list.append(cells[row][col])
                elif s_state_monster in cells[row][col].state:
                    monsters_cell_list.append(cells[row][col])

                # Pathway
                current = cells[row][col]
                map_graph[current] = []                             # Danh sách ô liền kề với ô hiện tại (current cell)

                if col - 1 >= 0 and map_matrix[row][col - 1] != 1:  # Tồn tại ô bên trái + ô bên trái là pathway
                    left = cells[row][col-1]  # Vị trí ô bên trái
                    map_graph[left] = map_graph[left] + [current]       # Thêm ô hiện tại vào danh sách kề ô bên trái
                    map_graph[current] = map_graph[current] + [left]    # Thêm ô bên trái vào danh sách kề ô hiện tại

                if row - 1 >= 0 and map_matrix[row - 1][col] != 1:  # Tồn tại ô bên trên + ô bên trên là pathway
                    up = cells[row-1][col]  # Vị trí ô bên trên
                    map_graph[up] = map_graph[up] + [current]           # Thêm ô hiện tại vào danh sách kề ô bên trên
                    map_graph[current] = map_graph[current] + [up]      # Thêm ô bên trên vào danh sách kề ô hiện tại

    return cells, map_graph,pacman_cell, food_cell_list, monsters_cell_list

