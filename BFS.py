import  queue
class Node:
    def __init__(self, state, path_cost, parent):
        self.state     = state
        self.path_cost = path_cost
        self.parent    = parent

    def __lt__(self, other):
        return self.path_cost < other.path_cost

def bfs_search(graph, pacman, food):
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

def ucs_search(graph, pacman, food):
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
