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
                    food_pos = (col, row)                                  #x = col, y = row from matrix -> oxy co-ordinate

                #Pathway
                current = (col, row)
                map_graph[current] = []                                    #Current cell's neighbors list

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
            if map_matrix[row][col] == 3:  # is monster
                monsters_pos_list.append((col, row))
                # Monster is Wall
                if fakewall: #if monster is considered as wall -> 1
                    map_matrix[row][col] = 1
                else:
                    map_matrix[row][col] = 0

    for row in range(len(map_matrix)):
        for col in range(len(map_matrix[row])):
            if map_matrix[row][col] != 1:                                  #Not wall
                # Food locator
                if map_matrix[row][col] == 2:                              #is food
                    food_pos = (col, row)                                     #x = col, y = row theo từ ma trận -> trục tọa độ

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
    print(map_matrix)
    return map_graph, pacman_pos, food_pos, monsters_pos_list

#LEVEL 3, 4 ------------------------------------------------------------------------------------------------------------
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
        if monster_index[1] - 1 > 0 and map_matrix[monster_index[0]][monster_index[1]-1] !=1:
            temp.append([monster_index[0],monster_index[1]-1])
        #Right
        if monster_index[1] + 1 < 28 and map_matrix[monster_index[0]][monster_index[1]+1] !=1:
            temp.append([monster_index[0],monster_index[1]+1])
        #Up
        if monster_index[0] - 1 > 0 and map_matrix[monster_index[0] - 1][monster_index[1]] !=1:
            temp.append([monster_index[0]-1,monster_index[1]])
        #Down
        if monster_index[0] + 1 < 28 and map_matrix[monster_index[0] + 1][monster_index[1]] !=1:
            temp.append([monster_index[0]+1,monster_index[1]])
        monster_list[monster_index] = temp

    return map_graph, (pacman_pos[0], pacman_pos[1]), food_pos, monster_list

def map_level4(path):
    file = open(path, "r")
    map_size = [int(val) for val in file.readline().split()]
    map_matrix = []
    for i in range(map_size[0]):
        map_matrix.append([int(val) for val in list(file.readline().split())])
    pacman_pos = [int(val) for val in list(file.readline().split())]

    food_pos = []
    monsters_pos_list = []

    # Declare graph map of pacman game
    map_graph = {}
    # row = y in co-ordinate
    # col = x in co-ordinate
    for row in range(len(map_matrix)):
        for col in range(len(map_matrix[row])):
            if map_matrix[row][col] == 3:  # Monster
                monsters_pos_list.append((row, col))
            # Not a wall: path & food
            if map_matrix[row][col] != 1:  # !Wall (Monster as Wall)
                # Food locator
                if map_matrix[row][col] == 2:
                    # food_pos = (col, row)                                  #x = col, y = row theo từ ma trận -> trục tọa độ
                    food_pos.append((row, col))
                # Pathway
                current = (row, col)
                map_graph[current] = []  # Danh sách ô liền kề với ô hiện tại (current cell)

                if col - 1 >= 0 and map_matrix[row][col - 1] != 1:  # Tồn tại ô bên trái + ô bên trái là pathway
                    left = (row, col - 1)  # Vị trí ô bên trái
                    map_graph[left] = map_graph[left] + [current]  # Thêm ô hiện tại vào danh sách kề ô bên trái
                    map_graph[current] = map_graph[current] + [left]  # Thêm ô bên trái vào danh sách kề ô hiện tại

                if row - 1 >= 0 and map_matrix[row - 1][col] != 1:  # Tồn tại ô bên trên + ô bên trên là pathway
                    up = (row - 1, col)  # Vị trí ô bên trên
                    map_graph[up] = map_graph[up] + [current]  # Thêm ô hiện tại vào danh sách kề ô bên trên
                    map_graph[current] = map_graph[current] + [up]
                    # Thêm ô bên trên vào danh sách kề ô hiện tại
    monster_list = {}
    for monster_index in monsters_pos_list:
        temp = []
        # Left
        if monster_index[1] - 1 > 0 and map_matrix[monster_index[0]][monster_index[1] - 1] != 1:
            temp.append([monster_index[0], monster_index[1] - 1])
        # Right
        if monster_index[1] + 1 < 28 and map_matrix[monster_index[0]][monster_index[1] + 1] != 1:
            temp.append([monster_index[0], monster_index[1] + 1])
        # Up
        if monster_index[0] - 1 > 0 and map_matrix[monster_index[0] - 1][monster_index[1]] != 1:
            temp.append([monster_index[0] - 1, monster_index[1]])
        # Down
        if monster_index[0] + 1 < 28 and map_matrix[monster_index[0] + 1][monster_index[1]] != 1:
            temp.append([monster_index[0] + 1, monster_index[1]])
        monster_list[monster_index] = temp
    return map_graph, (pacman_pos[0], pacman_pos[1]), food_pos, monster_list