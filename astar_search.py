#Level 1 and Level 2 searching
import queue

class Node:
    def __init__(self, state, path_cost, parent):
        self.state     = state
        self.path_cost = path_cost
        self.parent    = parent

    def __lt__(self, other):
        return self.path_cost < other.path_cost

def astar_search(graph, pacman, food):
    def heuristic(state, goal):
        dx = abs(state[0] - goal[0])
        dy = abs(state[1] - goal[1])
        return dx + dy

    visited    = set()
    frontier   = queue.PriorityQueue()                                #FRONTIER: Hàng đợi ưu tiên (Frontier) các node cần explore ^, giá trị priority là pathcost
    start_node = Node(pacman, heuristic(pacman, food), None)   #state - trạng thái ban đầu - pacman; path_cost - chi phí từ start đến goal; parent's state - trạng thái trước đó (Không có - None)

    frontier.put(start_node)                                          #Đặt node ban đầu (vị trí pacman ban đầu) vào hàng đợi
    visited.add(start_node.state)                                     #Đặt node ở trạng thái cần được khám phá, dict = tuple(x,y):trạng thái)

    while not frontier.empty():                                       #Chạy đến hết hàng đợi Frontier
        node = frontier.get()                                            #Lấy nút đầu tiên ở hàng đợi Frontier

        if node.state == food:                                           #Nếu vị trí (tuple(x,y)) hiện tại là goal, trả về kết quả bằng hàm pathway(danh sách đã explore)
            return pathway(node)                                           #Trả về là list

        for child_state in graph[node.state]:                           #For qua các node con của node hiện tại (từ node hiện tại có thể đi tới)
            child_node = Node(child_state, node.path_cost - heuristic(node.state, food) + 1 + heuristic(child_state, food), node)

            if child_node.state not in visited:
                frontier.put(child_node)
                visited.add(child_node.state)

    return None

def pathway(node):
    path = []
    while node:
        path.append(node.state)
        node = node.parent
    path.reverse()
    return path