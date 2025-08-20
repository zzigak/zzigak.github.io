# ==== RETRIEVED HELPER FUNCTIONS (NONE) ====

# ==== NEW HELPER FUNCTIONS ====
import sys
from heapq import heappush, heappop
from collections import deque

def read_ints():
    return map(int, sys.stdin.readline().split())

def build_adj_list(n, edges, undirected=True):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
        if undirected:
            adj[v].append((u, w))
    return adj

def dijkstra_with_path(n, adj, src, dest):
    INF = 10**24
    dist = [INF]*n
    parent = [-1]*n
    dist[src] = 0
    hq = [(0, src)]
    while hq:
        d, u = heappop(hq)
        if d > dist[u]:
            continue
        if u == dest:
            break
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                parent[v] = u
                heappush(hq, (nd, v))
    if dist[dest] >= INF:
        return None
    path = []
    u = dest
    while u != -1:
        path.append(u+1)
        u = parent[u]
    return path[::-1]

def dijkstra_two_hop(n, adj, src=0):
    INF = 10**24
    dist = [INF]*n
    dist[src] = 0
    hq = [(0, src)]
    while hq:
        d, u = heappop(hq)
        if d > dist[u]:
            continue
        for v, w1 in adj[u]:
            for x, w2 in adj[v]:
                nd = d + (w1 + w2)**2
                if nd < dist[x]:
                    dist[x] = nd
                    heappush(hq, (nd, x))
    return dist

def multi_source_bfs(n, rev_adj, sources):
    dist = [-1]*n
    dq = deque(sources)
    for s in sources:
        dist[s] = 0
    while dq:
        u = dq.popleft()
        for v in rev_adj[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                dq.append(v)
    return dist
