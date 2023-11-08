import queue

#Node class
class Node:
    def __init__(self, state, path_cost, parent):
        self.state     = state
        self.path_cost = path_cost
        self.parent    = parent

    def __lt__(self, other):
        return self.path_cost < other.path_cost

#BFS -------------------------------------------------------------------------------------------------------------------
def bfs(graph, pacman, food):
    visited = set()
    frontier = queue.Queue()
    start_node = Node(pacman, 0, None)

    frontier.put(start_node)
    visited.add(start_node.state)

    while not frontier.empty():
        node = frontier.get()

        if node.state == food:
            return pathway_bfs(node)

        for child_state in graph[node.state]:
            child_node = Node(child_state, node.path_cost + 1, node)

            if child_node.state not in visited:
                frontier.put(child_node)
                visited.add(child_node.state)

    return None

def pathway_bfs(node):
    path = []
    while node:
        path.append(node.state)
        node = node.parent
    path.reverse()
    return path

#DFS -------------------------------------------------------------------------------------------------------------------
def dfs_until(graph, start, end, visited, path):
    '''
    Input: graph,start position, end position,
    visited (to check if vetex visited), path (save path to pacman)
    Output: True if have path for pacman
    False if don't have path (then return Path for None)
    Loop via neighbor vertex of start, then use DFS them,
    until found path to food from pacman
    '''
    visited.add(start)
    path.append(start)

    if start == end:
        return True

    for neighbor in graph[start]:
        if neighbor not in visited:
            if dfs_until(graph, neighbor, end, visited, path):
                return True

    path.pop()
    return False


def dfs(graph, pacman, food):
    '''
    Input: graph, position of pacman, food
    Output: path None (If not), list of direction if exist
    use DFS_until until find pathway
    '''
    # Set of visited nodes and path for run
    visited = set()
    path = []
    dfs_until(graph, pacman, food, visited, path)
    if not path:
        return None
    return path

#UCS -------------------------------------------------------------------------------------------------------------------
def ucs(graph, pacman, food):
    visited = set()
    frontier = queue.PriorityQueue()
    start_node = Node(pacman, 0, None)

    frontier.put(start_node)
    visited.add(start_node.state)

    while not frontier.empty():
        node = frontier.get()

        if node.state == food:
            return pathway_ucs(node)

        for child_state in graph[node.state]:
            child_node = Node(child_state, node.path_cost + 1, node)

            if child_node.state not in visited:
                frontier.put(child_node)
                visited.add(child_node.state)
    return None

def pathway_ucs(node):
    path = []
    while node:
        path.append(node.state)
        node = node.parent
    path.reverse()
    return path