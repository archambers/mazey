from heapq import heappush, heappop
from collections import deque


def rtdfs(start, end, adj):
    stack = [start]
    visited = set()
    path = {}
    while stack:
        curr = stack.pop()
        visited.add(curr)
        nbrs = []
        for neighbor in adj[curr]:
            if neighbor not in visited:
                stack.append(neighbor)
                path[neighbor] = curr
                nbrs.append(neighbor)
        yield (curr, nbrs, path)


def rtbfs(start, end, adj):
    stack = deque()
    stack.append(start)
    visited = set()
    path = {}
    while stack:
        curr = stack.popleft()
        visited.add(curr)
        nbrs = []
        for neighbor in adj[curr]:
            if neighbor not in visited:
                stack.append(neighbor)
                path[neighbor] = curr
                nbrs.append(neighbor)
        yield (curr, nbrs, path)


def calc_dist(now, end):
    return (abs(end.x - now.x) + abs(end.y - now.y))


def rtastar(start, end, adj):
    heap = [(calc_dist(start, end), 0, 0, start)]
    visited = set()
    path = {}
    count = 0
    while heap:
        curr_left, curr_sofar, _, curr = heappop(heap)
        visited.add(curr)
        nbrs = []
        for neighbor in adj[curr]:
            if neighbor not in visited:
                heappush(heap, (curr_sofar + calc_dist(neighbor, end),
                                curr_sofar + 1, count, neighbor))
                path[neighbor] = curr
                nbrs.append(neighbor)
                count += 1
        yield (curr, nbrs, path)
