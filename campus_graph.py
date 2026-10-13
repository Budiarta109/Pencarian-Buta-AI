import heapq
from collections import deque

CAMPUS_GRAPH = {
    "Main Gate": {"Library": 3, "Cafeteria": 5, "Admin Building": 2},
    "Library": {"Main Gate": 3, "Science Lab": 4, "Computer Center": 6, "Student Center": 3},
    "Cafeteria": {"Main Gate": 5, "Sports Complex": 4, "Student Center": 2},
    "Admin Building": {"Main Gate": 2, "Lecture Hall A": 3, "Parking Lot": 4},
    "Science Lab": {"Library": 4, "Lecture Hall A": 2, "Engineering Block": 5},
    "Computer Center": {"Library": 6, "Engineering Block": 3, "Auditorium": 4},
    "Student Center": {"Library": 3, "Cafeteria": 2, "Auditorium": 5, "Dormitory": 3},
    "Sports Complex": {"Cafeteria": 4, "Dormitory": 6, "Parking Lot": 3},
    "Lecture Hall A": {"Admin Building": 3, "Science Lab": 2, "Lecture Hall B": 2},
    "Lecture Hall B": {"Lecture Hall A": 2, "Engineering Block": 3, "Auditorium": 4},
    "Engineering Block": {"Science Lab": 5, "Computer Center": 3, "Lecture Hall B": 3},
    "Auditorium": {"Computer Center": 4, "Student Center": 5, "Lecture Hall B": 4},
    "Dormitory": {"Student Center": 3, "Sports Complex": 6, "Parking Lot": 5},
    "Parking Lot": {"Admin Building": 4, "Sports Complex": 3, "Dormitory": 5},
}

NODE_POSITIONS = {
    "Main Gate":         {"x": 100, "y": 360},
    "Admin Building":    {"x": 240, "y": 520},
    "Library":           {"x": 260, "y": 200},
    "Cafeteria":         {"x": 290, "y": 370},
    "Science Lab":       {"x": 450, "y": 100},
    "Computer Center":   {"x": 510, "y": 240},
    "Student Center":    {"x": 480, "y": 380},
    "Sports Complex":    {"x": 390, "y": 570},
    "Parking Lot":       {"x": 240, "y": 670},
    "Dormitory":         {"x": 570, "y": 620},
    "Lecture Hall A":    {"x": 600, "y": 490},
    "Lecture Hall B":    {"x": 730, "y": 430},
    "Engineering Block": {"x": 710, "y": 140},
    "Auditorium":        {"x": 840, "y": 310},
}


def bfs(graph, start, goal):
    if start == goal:
        return [start], [start], 0, []

    visited = []
    explored_edges = []
    queue = deque()
    queue.append((start, [start]))

    while queue:
        current, path = queue.popleft()
        if current in visited:
            continue
        visited.append(current)

        for neighbor in sorted(graph[current].keys()):
            if neighbor not in visited:
                explored_edges.append({"from": current, "to": neighbor})
                new_path = path + [neighbor]
                if neighbor == goal:
                    visited.append(neighbor)
                    total = sum(
                        graph[new_path[i]][new_path[i + 1]]
                        for i in range(len(new_path) - 1)
                    )
                    return new_path, visited, total, explored_edges
                queue.append((neighbor, new_path))

    return None, visited, 0, explored_edges


def dfs(graph, start, goal):
    if start == goal:
        return [start], [start], 0, []

    visited = []
    explored_edges = []
    stack = [(start, [start])]

    while stack:
        current, path = stack.pop()
        if current in visited:
            continue
        visited.append(current)

        if current == goal:
            total = sum(
                graph[path[i]][path[i + 1]] for i in range(len(path) - 1)
            )
            return path, visited, total, explored_edges

        for neighbor in sorted(graph[current].keys(), reverse=True):
            if neighbor not in visited:
                explored_edges.append({"from": current, "to": neighbor})
                stack.append((neighbor, path + [neighbor]))

    return None, visited, 0, explored_edges


def ucs(graph, start, goal):
    if start == goal:
        return [start], [start], 0, []

    visited = []
    explored_edges = []
    counter = 0
    heap = [(0, counter, start, [start])]

    while heap:
        cost, _, current, path = heapq.heappop(heap)
        if current in visited:
            continue
        visited.append(current)

        if current == goal:
            return path, visited, cost, explored_edges

        for neighbor in sorted(graph[current].keys()):
            if neighbor not in visited:
                explored_edges.append({"from": current, "to": neighbor})
                new_cost = cost + graph[current][neighbor]
                counter += 1
                heapq.heappush(heap, (new_cost, counter, neighbor, path + [neighbor]))

    return None, visited, 0, explored_edges


def dls(graph, start, goal, depth_limit):
    if start == goal:
        return [start], [start], 0, [], False

    visited = []
    explored_edges = []
    cutoff_occurred = False
    stack = [(start, [start], 0)]

    while stack:
        current, path, depth = stack.pop()
        if current in visited:
            continue
        visited.append(current)

        if current == goal:
            total = sum(
                graph[path[i]][path[i + 1]] for i in range(len(path) - 1)
            )
            return path, visited, total, explored_edges, False

        if depth >= depth_limit:
            cutoff_occurred = True
            visited.pop()
            continue

        for neighbor in sorted(graph[current].keys(), reverse=True):
            if neighbor not in visited:
                explored_edges.append({"from": current, "to": neighbor})
                stack.append((neighbor, path + [neighbor], depth + 1))

    return None, visited, 0, explored_edges, cutoff_occurred


def ids(graph, start, goal, max_depth=20):
    if start == goal:
        return [start], [start], 0, [], 0

    all_visited = []
    all_explored_edges = []

    for depth_limit in range(max_depth + 1):
        path, visited, cost, edges, cutoff = dls(graph, start, goal, depth_limit)
        all_visited = visited
        all_explored_edges = edges
        if path is not None:
            return path, all_visited, cost, all_explored_edges, depth_limit
        if not cutoff:
            break

    return None, all_visited, 0, all_explored_edges, max_depth


def get_all_locations():
    return sorted(CAMPUS_GRAPH.keys())
