import queue
from constant_value import *
from collections import deque

def astar_search(graph, pacman, food):
    def heuristic(state, goal):  #Diagonal
        dx = abs(state[0] - goal[0])
        dy = abs(state[1] - goal[1])
        return dx + dy - min(dx, dy)

    visited = {}                                     #VISITED dict : dictionary chứa tuple(địa chỉ node):trạng thái
    for state in graph:
        visited[state] = node_NotVisited                #Đánh dấu tất cả node_NotVisited

    node = (heuristic(pacman, food), pacman, None)      #node = (path cost, state, parent's state) - node mới với 3 giá trị: path_cost - chi phí từ start đến goal; state - trạng thái hiện tại (ban đầu - pacman); parent's state - trạng thái trước đó (Không có - None)
    frontier = queue.PriorityQueue()                 #FRONTIER     : Hàng đợi ưu tiên (Frontier) các node cần explore ^, giá trị priority là pathcost
    explored = []                                    #EXPLORED list: Các node đã explore, ban đầu = [], mỗi giá trị ứng với (vị trí node hiện tại, vị trí node cha)

    frontier.put(node)                               #Đặt node ban đầu (vị trí pacman ban đầu) vào hàng đợi
    visited[node[1]] = node_Frontier                 #Đặt node ở trạng thái cần được khám phá, dict = tuple(x,y):trạng thái

    while frontier.queue:                            #Chạy đến hết hàng đợi Frontier
        node = frontier.get()                           #Lấy nút đầu tiên ở hàng đợi Frontier
        explored.append((node[1], node[2]))             #Đặt giá trị vào danh sách đã khám phá, gồm tuple(vị trí node hiện tại, vị trí node cha)
        visited[node[1]] = node_Explored                #Đặt trạng thái node đã explore

        if node[1] == food:                             #Nếu vị trí (tuple(x,y)) hiện tại là goal, trả về kết quả bằng hàm pathway(danh sách đã explore)
            return pathway(explored)                        #Trả về là list

        for child_state in graph[node[1]]:                  #For qua các node con của node hiện tại (từ node hiện tại có thể đi tới)
            h_state = heuristic(node[1], food)                  #h_state       : ước tính chi phí của trạng thái hiện tại -> food = heuristic()
            h_child_state = heuristic(child_state, food)        #h_child_state : ước tính chi phí của con trạng thái hiện tại -> food = heuristic()

            if visited[child_state] == node_NotVisited:                                         #Nếu node con = chưa visited (chưa ở trong Frontier)
                frontier.put((node[0] - h_state + 1 + h_child_state, child_state, node[1]))         #Bỏ vào Frontier(pathcost = pathcost từ start->goal - pathcost từ hiện tại->goal (=pathcost từ start->current) + 1 (=pathcost từ current->node con) + pathcost node con->goal ; vị trí node con ; node cha = node hiện tại)
                visited[child_state] = node_Frontier                                                #Đặt trạng thái Frontier
            elif visited[child_state] == node_Frontier:                                         #Nếu đã ở trong Frontier: cập nhập lại pathcost
                update(frontier, (node[0] - h_state + 1 + h_child_state, child_state, node[1]))

    print("return none?")
    return None

def pathway(explored):
    parent_table = dict()                   #Tạo dict là node cha của node con
    for node in explored:                   #tuple(vị trí node hiện tại, vị trí node cha)
        parent_table[node[0]] = node[1]     #dict = node hiện tại:node cha

    state, parent_state = explored[-1][0], explored[-1][1]  #state: node goal, parent_state: node cha của goal
    path = deque([state])                                   #path = hàng đợi kiểu deque với 1 giá trị [state] là giá trị node goal
    while parent_state is not None:                         #chạy đến khi node cha = node, nghĩa là node đó là node start
        state = parent_state                                    #stae = Lấy node cha
        parent_state = parent_table[state]                      #node cha của state = lấy từ dict cha
        path.appendleft(state)                                  #bỏ vào bên trái hàng đợi

    return list(path)                       #Trả về list là path từ node start -> goal

def update(frontier, node):
    temp_frontier = []
    while frontier.queue:
        temp_frontier.append(frontier.get())

    for temp_node in temp_frontier:
        if temp_node[1] == node[1]:
            if temp_node[0] > node[0]:
                temp_node = node
        frontier.put(temp_node)

#BACKUP
# def astar_search(graph, pacman, food):
#     def heuristic(state, goal):  # Manhattan
#         return int(abs(state[0] - goal[0]) + abs(state[1] - goal[1]))
#
#     visited = {}                                     #VISITED dict : dictionary chứa tuple(địa chỉ node):trạng thái
#     for state in graph:
#         visited[state] = node_NotVisited                #Đánh dấu tất cả node_NotVisited
#
#     node = (heuristic(pacman, food), pacman, None)      #node = (path cost, state, parent's state) - node mới với 3 giá trị: path_cost - chi phí từ start đến goal; state - trạng thái hiện tại (ban đầu - pacman); parent's state - trạng thái trước đó (Không có - None)
#     frontier = queue.PriorityQueue()                 #FRONTIER     : Hàng đợi ưu tiên (Frontier) các node cần explore ^, giá trị priority là pathcost
#     explored = []                                    #EXPLORED list: Các node đã explore, ban đầu = [], mỗi giá trị ứng với (vị trí node hiện tại, vị trí node cha)
#
#     frontier.put(node)                               #Đặt node ban đầu (vị trí pacman ban đầu) vào hàng đợi
#     visited[node[1]] = node_Frontier                 #Đặt node ở trạng thái cần được khám phá, dict = tuple(x,y):trạng thái
#
#     while frontier.queue:                            #Chạy đến hết hàng đợi Frontier
#         node = frontier.get()                           #Lấy nút đầu tiên ở hàng đợi Frontier
#         explored.append((node[1], node[2]))             #Đặt giá trị vào danh sách đã khám phá, gồm tuple(vị trí node hiện tại, vị trí node cha)
#         visited[node[1]] = node_Explored                #Đặt trạng thái node đã explore
#
#         if node[1] == food:                             #Nếu vị trí (tuple(x,y)) hiện tại là goal, trả về kết quả bằng hàm pathway(danh sách đã explore)
#             return pathway(explored)                        #Trả về là list
#
#         for child_state in graph[node[1]]:                  #For qua các node con của node hiện tại (từ node hiện tại có thể đi tới)
#             h_state = heuristic(node[1], food)                  #h_state       : ước tính chi phí của trạng thái hiện tại -> food = heuristic()
#             h_child_state = heuristic(child_state, food)        #h_child_state : ước tính chi phí của con trạng thái hiện tại -> food = heuristic()
#
#             if visited[child_state] == node_NotVisited:                                         #Nếu node con = chưa visited (chưa ở trong Frontier)
#                 frontier.put((node[0] - h_state + 1 + h_child_state, child_state, node[1]))         #Bỏ vào Frontier(pathcost = pathcost từ start->goal - pathcost từ hiện tại->goal (=pathcost từ start->current) + 1 (=pathcost từ current->node con) + pathcost node con->goal ; vị trí node con ; node cha = node hiện tại)
#                 visited[child_state] = node_Frontier                                                #Đặt trạng thái Frontier
#             elif visited[child_state] == node_Frontier:                                         #Nếu đã ở trong Frontier: cập nhập lại pathcost
#                 update(frontier, (node[0] - h_state + 1 + h_child_state, child_state, node[1]))
#
#     return None
#
# def pathway(explored):
#     parent_table = dict()                   #Tạo dict là node cha của node con
#     for node in explored:                   #tuple(vị trí node hiện tại, vị trí node cha)
#         parent_table[node[0]] = node[1]     #dict = node hiện tại:node cha
#
#     state, parent_state = explored[-1][0], explored[-1][1]  #state: node goal, parent_state: node cha của goal
#     path = deque([state])                                   #path = hàng đợi kiểu deque với 1 giá trị [state] là giá trị node goal
#     while parent_state is not None:                         #chạy đến khi node cha = node, nghĩa là node đó là node start
#         state = parent_state                                    #stae = Lấy node cha
#         parent_state = parent_table[state]                      #node cha của state = lấy từ dict cha
#         path.appendleft(state)                                  #bỏ vào bên trái hàng đợi
#
#     return list(path)                       #Trả về list là path từ node start -> goal
#
# def update(frontier, node):
#     temp_frontier = []
#     while frontier.queue:
#         temp_frontier.append(frontier.get())
#
#     for temp_node in temp_frontier:
#         if temp_node[1] == node[1]:
#             if temp_node[0] > node[0]:
#                 temp_node = node
#         frontier.put(temp_node)