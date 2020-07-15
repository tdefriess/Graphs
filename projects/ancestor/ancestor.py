class Stack():
    def __init__(self):
        self.stack = []
    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def size(self):
        return len(self.stack)
class Graph:
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex_id):
        self.vertices[vertex_id] = set()

    def add_edge(self, v1, v2):
        self.vertices[v1].add(v2)

    def get_neighbors(self, vertex_id):
        return self.vertices[vertex_id]

    def dfs(self, starting_vertex, destination_vertex):
        stack = Stack()
        stack.push(starting_vertex)
        path = []

        visited = set()

        while stack.size() > 0:
            current_node = stack.pop()

            if current_node not in visited:
                visited.add(current_node)
                path.append(current_node)

                if current_node == destination_vertex:
                    return path

                neighbors = self.get_neighbors(current_node)
                for neighbor in neighbors:
                    stack.push(neighbor)


def earliest_ancestor(ancestors, starting_node):
    graph = Graph()

    for ancestor in ancestors:
        for vertex in ancestor:
            graph.add_vertex(vertex)
        graph.add_edge(ancestor[0], ancestor[1])

    stack = Stack()
    stack.push( starting_node)

    paths = []
    oldest = -1
    longest_path = 0

    for vertex in graph.vertices:
        search_path = graph.dfs(vertex, starting_node)
        paths = paths + [search_path]

    for path in paths:
        if path is not None:
            if len(path) > longest_path:
                longest_path = len(path)
                oldest = path[0]
            elif len(path) == longest_path and len(path) > 0:
                if path[0] < oldest:
                    oldest = path[0]

            return oldest