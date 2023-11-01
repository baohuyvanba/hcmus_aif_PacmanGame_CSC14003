import localsearch as ls
from constant_value import *

#LEVEL 1, 2 ------------------------------------------------------------------------------------------------------------
def map_level1(path):
    file = open(path, "r")
    map_size = [int(val) for val in file.readline().split()]
    map_matrix = []
    for i in range(map_size[0]):
        map_matrix.append([int(val) for val in list(file.readline().split())])
    pacman_pos_list = [int(val) for val in list(file.readline().split())]
    pacman_pos = (pacman_pos_list[0], pacman_pos_list[1])
    food_pos = None

    #Declare graph map of possible pathway
    map_graph = {}
        #row = y in co-ordinate
        #col = x in co-ordinate
    for row in range(len(map_matrix)):
        for col in range(len(map_matrix[row])):
            #Not a wall: path & food
            if map_matrix[row][col] != 1:
                #Food locator
                if map_matrix[row][col] == 2:
                    food_pos = (col, row)                              #x = col, y = row theo từ ma trận -> trục tọa độ

                #Pathway
                current = (col, row)
                map_graph[current] = []                                #Danh sách ô liền kề với ô hiện tại (current cell)

                if col - 1 >= 0 and map_matrix[row][col - 1] != 1:         #Tồn tại ô bên trái + ô bên trái là pathway
                    left = (col - 1, row)                                      #Vị trí ô bên trái
                    map_graph[left]    = map_graph[left] + [current]           #Thêm ô hiện tại vào danh sách kề ô bên trái
                    map_graph[current] = map_graph[current] + [left]           #Thêm ô bên trái vào danh sách kề ô hiện tại

                if row - 1 >= 0 and map_matrix[row - 1][col] != 1:         #Tồn tại ô bên trên + ô bên trên là pathway
                    up = (col, row - 1)                                        #Vị trí ô bên trên
                    map_graph[up]      = map_graph[up] + [current]             #Thêm ô hiện tại vào danh sách kề ô bên trên
                    map_graph[current] = map_graph[current] + [up]             #Thêm ô bên trên vào danh sách kề ô hiện tại

    return map_graph, pacman_pos, food_pos

def map_level2(path, fakewall: bool):
    file = open(path, "r")
    map_size = [int(val) for val in file.readline().split()]
    map_matrix = []
    for i in range(map_size[0]):
        map_matrix.append([int(val) for val in list(file.readline().split())])
    pacman_pos_list = [int(val) for val in list(file.readline().split())]
    pacman_pos = (pacman_pos_list[0], pacman_pos_list[1])

    food_pos = None
    monsters_pos_list = []

    #Declare graph map of possible
    map_graph = {}
        #row = y in co-ordinate
        #col = x in co-ordinate
    for row in range(len(map_matrix)):
        for col in range(len(map_matrix[row])):
            if map_matrix[row][col] != 1:                                  #Not wall
                # Food locator
                if map_matrix[row][col] == 2:                              #is food
                    food_pos = (col, row)                                     #x = col, y = row theo từ ma trận -> trục tọa độ
                elif map_matrix[row][col] == 3:                            #is monster
                    monsters_pos_list.append((col, row))
                    # Monster is Wall
                    if fakewall:
                        map_matrix[row][col] = 1                           #if monster is considered as wall -> 1

                #Pathway
                current = (col, row)
                map_graph[current] = []                                    #Danh sách ô liền kề với ô hiện tại (current cell)

                if col - 1 >= 0 and map_matrix[row][col - 1] != 1:         #Tồn tại ô bên trái + ô bên trái là pathway
                    left = (col - 1, row)                                    #Vị trí ô bên trái
                    map_graph[left]    = map_graph[left] + [current]          #Thêm ô hiện tại vào danh sách kề ô bên trái
                    map_graph[current] = map_graph[current] + [left]          #Thêm ô bên trái vào danh sách kề ô hiện tại

                if row - 1 >= 0 and map_matrix[row - 1][col] != 1:         #Tồn tại ô bên trên + ô bên trên là pathway
                    up = (col, row - 1)                                      #Vị trí ô bên trên
                    map_graph[up]      = map_graph[up] + [current]            #Thêm ô hiện tại vào danh sách kề ô bên trên
                    map_graph[current] = map_graph[current] + [up]            #Thêm ô bên trên vào danh sách kề ô hiện tại

    return map_graph, pacman_pos, food_pos, monsters_pos_list


#LEVEL 3, 4 ------------------------------------------------------------------------------------------------------------

#Build Cell: build a matrix of Cell (Cell is a self-implementing datatype (in localsearch.py))
def build_cell(matrix_map, pacman_pos):
    cells = []
        #y = row, x = col
    for row in range(len(matrix_map)):
        temp = []
        for col in range(len(matrix_map[row])):
            #Not wall
            if matrix_map[row][col] != 1:
                #Add state to Cell's state list:
                if matrix_map[row][col]   == 0:                                               #Cell with blank pathway
                    temp.append(ls.Cell((col, row), []))
                elif matrix_map[row][col] == 2:                                               #Cell with food
                    temp.append(ls.Cell((col, row), [s_state_food]))
                elif matrix_map[row][col] == 3:                                               #Cell with monster
                    temp.append(ls.Cell((col, row), [s_state_monster]))

                #If pacman is on a Cell, add pacman state to Cell's state list:
                if (col, row) == pacman_pos:
                    temp[col].state.append(s_state_pacman)
                    pacman_cell = temp[col]                                                   #Save pacman cell

            #Pacman / Monsters can stay in a wall :>
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
    pacman_pos = [int(val) for val in list(file.readline().split())]

    food_pos = []
    monsters_pos_list = []

    #Declare graph map of pacman game
    map_graph = {}
        #row = y in co-ordinate
        #col = x in co-ordinate
    for row in range(len(map_matrix)):
        for col in range(len(map_matrix[row])):
            if map_matrix[row][col] == 3:                                  #Monster
                monsters_pos_list.append((row, col))
            #Not a wall: path & food
            if map_matrix[row][col] != 1:
                #Food locator
                if map_matrix[row][col] == 2:
                    # food_pos = (col, row)                                  #x = col, y = row theo từ ma trận -> trục tọa độ
                    food_pos.append((row,col))
                #Pathway
                current = (row, col)
                map_graph[current] = []                                    #Danh sách ô liền kề với ô hiện tại (current cell)

                if col - 1 >= 0 and map_matrix[row][col - 1] != 1 :         #Tồn tại ô bên trái + ô bên trái là pathway
                    left = (row,col - 1) #Vị trí ô bên trái
                    map_graph[left]    = map_graph[left] + [current]       #Thêm ô hiện tại vào danh sách kề ô bên trái
                    map_graph[current] = map_graph[current] + [left]       #Thêm ô bên trái vào danh sách kề ô hiện tại

                if row - 1 >= 0 and map_matrix[row - 1][col] != 1 :         #Tồn tại ô bên trên + ô bên trên là pathway
                    up = (row - 1,col)  #Vị trí ô bên trên
                    map_graph[up]      = map_graph[up] + [current]         #Thêm ô hiện tại vào danh sách kề ô bên trên
                    map_graph[current] = map_graph[current] + [up]
                          #Thêm ô bên trên vào danh sách kề ô hiện tại
    monster_list = {}
    for monster_index in monsters_pos_list:
        temp = []
        #Left
        if monster_index[1] - 1 > 0 and map_matrix[monster_index[0]][monster_index[1]-1]!=1:
            temp.append([monster_index[0],monster_index[1]-1])
        #Right
        if monster_index[1] + 1<28 and map_matrix[monster_index[0]][monster_index[1]+1]!=1:
            temp.append([monster_index[0],monster_index[1]+1])
        #Up
        if monster_index[0] - 1>0 and map_matrix[monster_index[0] - 1][monster_index[1]]!=1:
            temp.append([monster_index[0]-1,monster_index[1]])
        #Down
        if monster_index[0] + 1<28 and map_matrix[monster_index[0] + 1][monster_index[1]]!=1:
            temp.append([monster_index[0]+1,monster_index[1]])
        monster_list[monster_index] = temp

    return map_graph, (pacman_pos[0], pacman_pos[1]), food_pos, monster_list


def map_level4(path):
    #Read txt file to matrix
    file = open(path, "r")
    map_size = [int(val) for val in file.readline().split()]
    map_matrix = []
    for i in range(map_size[0]):
        map_matrix.append([int(val) for val in list(file.readline().split())])
    pacman_pos_list = [int(val) for val in list(file.readline().split())]
    pacman_pos = (pacman_pos_list[0], pacman_pos_list[1])

    #Build Cells matrix
    cells, pacman_cell = build_cell(map_matrix, pacman_pos)

    food_cell_list = []
    monsters_cell_list = []
    map_graph = {}
    ori_map_graph = {}
        # row = y in co-ordinate
        # col = x in co-ordinate
    for row in range(len(map_matrix)):
        for col in range(len(map_matrix[row])):
            if map_matrix[row][col] != 1:                        #Not wall
                #Food
                if s_state_food in cells[row][col].state:
                    food_cell_list.append(cells[row][col])          # Add Cell with Food to food_list
                elif s_state_monster in cells[row][col].state:
                    monsters_cell_list.append(cells[row][col])      # Add Cell with Monster to monster_list

                # Pathway
                current = cells[row][col]
                map_graph[current] = []                             # Danh sách ô liền kề với ô hiện tại (current cell)

                if col - 1 >= 0 and map_matrix[row][col - 1] != 1:  # Tồn tại ô bên trái + ô bên trái là pathway
                    left = cells[row][col-1]                            # Vị trí ô bên trái
                    map_graph[left] = map_graph[left] + [current]       # Thêm ô hiện tại vào danh sách kề ô bên trái
                    map_graph[current] = map_graph[current] + [left]    # Thêm ô bên trái vào danh sách kề ô hiện tại

                if row - 1 >= 0 and map_matrix[row - 1][col] != 1:  # Tồn tại ô bên trên + ô bên trên là pathway
                    up = cells[row-1][col]                              # Vị trí ô bên trên
                    map_graph[up] = map_graph[up] + [current]           # Thêm ô hiện tại vào danh sách kề ô bên trên
                    map_graph[current] = map_graph[current] + [up]      # Thêm ô bên trên vào danh sách kề ô hiện tại

                #original map graph
                ori_current = (col, row)
                ori_map_graph[ori_current] = []
                if col - 1 >= 0 and map_matrix[row][col - 1] != 1:                  #Tồn tại ô bên trái + ô bên trái là pathway
                    ori_left = (col - 1, row)                                               #Vị trí ô bên trái
                    ori_map_graph[ori_left]    = ori_map_graph[ori_left] + [ori_current]    #Thêm ô hiện tại vào danh sách kề ô bên trái
                    ori_map_graph[ori_current] = ori_map_graph[ori_current] + [ori_left]    #Thêm ô bên trái vào danh sách kề ô hiện tại

                if row - 1 >= 0 and map_matrix[row - 1][col] != 1:                  #Tồn tại ô bên trên + ô bên trên là pathway
                    ori_up = (col, row - 1)                                                 #Vị trí ô bên trên
                    ori_map_graph[ori_up]      = ori_map_graph[ori_up] + [ori_current]      #Thêm ô hiện tại vào danh sách kề ô bên trên
                    ori_map_graph[ori_current] = ori_map_graph[ori_current] + [ori_up]      #Thêm ô bên trên vào danh sách kề ô hiện tại

    return cells, map_graph, ori_map_graph, pacman_cell, food_cell_list, monsters_cell_list