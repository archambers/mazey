from heapq import heappush, heappop
from collections import deque
from constants import *
from math import sqrt


def get_neighbors(grid, curr):
    neighbors = set()
    x, y = curr.x, curr.y
    if y > 0:
        if grid[y - 1][x].color != WALL:
            neighbors.add(grid[y - 1][x])
        # if x > 0:
        #     if grid[y - 1][x - 1].color != WALL:
        #         neighbors.add(grid[y - 1][x - 1])
        # if x < COLS - 1:
        #     if grid[y - 1][x + 1].color != WALL:
        #         neighbors.add(grid[y - 1][x + 1])
    if y < ROWS - 1:
        if grid[y + 1][x].color != WALL:
            neighbors.add(grid[y + 1][x])
        # if x > 0:
        #     if grid[y + 1][x - 1].color != WALL:
        #         neighbors.add(grid[y + 1][x - 1])
        # if x < COLS - 1:
        #     if grid[y + 1][x + 1].color != WALL:
        #         neighbors.add(grid[y + 1][x + 1])
    if x > 0:
        if grid[y][x - 1].color != WALL:
            neighbors.add(grid[y][x - 1])
    if x < COLS - 1:
        if grid[y][x + 1].color != WALL:
            neighbors.add(grid[y][x + 1])
    return neighbors


def rtdfs(start, end, adj):
    stack = [start]
    visited = set()
    path = {}
    while stack:
        curr = stack.pop()
        visited.add(curr)
        nbrs = []
        # for neighbor in adj[curr]:
        for neighbor in get_neighbors(adj, curr):
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
        # for neighbor in adj[curr]:
        for neighbor in get_neighbors(adj, curr):
            if neighbor not in visited:
                stack.append(neighbor)
                path[neighbor] = curr
                nbrs.append(neighbor)
        yield (curr, nbrs, path)


def calc_dist(now, end):
    return (abs(end.x - now.x) + abs(end.y - now.y))


def pythag(now, end):
    return sqrt((end.x - now.x)**2 + (end.y - now.y)**2)


def rtastarm(start, end, adj):
    heap = [(calc_dist(start, end), 0, 0, start)]
    visited = set()
    path = {}
    count = 0
    while heap:
        curr_left, curr_sofar, _, curr = heappop(heap)
        visited.add(curr)
        nbrs = []
        # for neighbor in adj[curr]:
        for neighbor in get_neighbors(adj, curr):
            if neighbor not in visited:
                heappush(heap, (curr_sofar + pythag(neighbor, end),
                                curr_sofar + pythag(curr, neighbor), count, neighbor))
                path[neighbor] = curr
                nbrs.append(neighbor)
                count -= 1
        yield (curr, nbrs, path)

def rtastar(start, end, adj):
    heap = [(calc_dist(start, end), 0, 0, start)]
    visited = set()
    path = {}
    count = 0
    while heap:
        curr_left, curr_sofar, _, curr = heappop(heap)
        visited.add(curr)
        nbrs = []
        # for neighbor in adj[curr]:
        for neighbor in get_neighbors(adj, curr):
            if neighbor not in visited:
                heappush(heap, (curr_sofar + calc_dist(neighbor, end),
                                curr_sofar + 1, count, neighbor))
                path[neighbor] = curr
                nbrs.append(neighbor)
                count -= 1
        yield (curr, nbrs, path)
