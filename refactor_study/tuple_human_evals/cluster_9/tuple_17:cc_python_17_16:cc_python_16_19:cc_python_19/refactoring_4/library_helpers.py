# ==== RETRIEVED HELPER FUNCTIONS (NONE) ====

# ==== NEW HELPER FUNCTIONS ====
import heapq
from collections import deque

def read_ints():
    return list(map(int, input().split()))

def build_adj_list(n, edges):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))
    return adj

def shortest_path(adj, src, dest):
    INF = 10**18
    n = len(adj)
    dist = [INF]*n
    parent = [-1]*n
    dist[src] = 0
    heap = [(0, src)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        if u == dest:
            break
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                parent[v] = u
                heapq.heappush(heap, (nd, v))
    if dist[dest] == INF:
        return None
    path = []
    cur = dest
    while cur != -1:
        path.append(cur+1)
        cur = parent[cur]
    return path[::-1]

def two_step_dijkstra(adj):
    INF = 10**18
    n = len(adj)
    dist = [INF]*n
    dist[0] = 0
    heap = [(0, 0)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for v, w1 in adj[u]:
            for x, w2 in adj[v]:
                nd = d + (w1 + w2)**2
                if nd < dist[x]:
                    dist[x] = nd
                    heapq.heappush(heap, (nd, x))
    return dist

def build_rev_graph_and_seeds(a):
    n = len(a)
    rev = [[] for _ in range(n)]
    seeds = []
    for i, val in enumerate(a):
        for j in (i+val, i-val):
            if 0 <= j < n:
                if (a[j] & 1) != (val & 1):
                    seeds.append(i)
                else:
                    rev[j].append(i)
    return rev, seeds

def bfs_from_seeds(graph, seeds):
    ans = [-1]*len(graph)
    dq = deque()
    for s in seeds:
        if ans[s] == -1:
            ans[s] = 1
            dq.append(s)
    while dq:
        u = dq.popleft()
        for v in graph[u]:
            if ans[v] == -1:
                ans[v] = ans[u] + 1
                dq.append(v)
    return ans
