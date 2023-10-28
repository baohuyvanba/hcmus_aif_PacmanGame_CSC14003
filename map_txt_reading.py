
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

def map_level2(path):
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
            if map_matrix[row][col] == 3:                                  #Monster
                monsters_pos_list.append((col, row))
            #Not a wall: path & food
            if map_matrix[row][col] != 1 and map_matrix[row][col] != 3:    #!Monster vs !Wall (Monster as Wall)
                #Food locator
                if map_matrix[row][col] == 2:
                    food_pos = (col, row)                                  #x = col, y = row theo từ ma trận -> trục tọa độ
                #Pathway
                current = (col, row)
                map_graph[current] = []                                    #Danh sách ô liền kề với ô hiện tại (current cell)

                if col - 1 >= 0 and map_matrix[row][col - 1] != 1 and map_matrix[row][col - 1] != 3:         #Tồn tại ô bên trái + ô bên trái là pathway
                    left = (col - 1, row) #Vị trí ô bên trái
                    map_graph[left]    = map_graph[left] + [current]       #Thêm ô hiện tại vào danh sách kề ô bên trái
                    map_graph[current] = map_graph[current] + [left]       #Thêm ô bên trái vào danh sách kề ô hiện tại

                if row - 1 >= 0 and map_matrix[row - 1][col] != 1 and map_matrix[row][col - 1] != 3:         #Tồn tại ô bên trên + ô bên trên là pathway
                    up = (col, row - 1)  #Vị trí ô bên trên
                    map_graph[up]      = map_graph[up] + [current]         #Thêm ô hiện tại vào danh sách kề ô bên trên
                    map_graph[current] = map_graph[current] + [up]         #Thêm ô bên trên vào danh sách kề ô hiện tại

    return map_graph, (pacman_pos[0], pacman_pos[1]), food_pos, monsters_pos_list
