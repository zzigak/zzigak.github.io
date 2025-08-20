# ########## LIBRARY HELPERS ##########

# ==== RETRIEVED HELPER FUNCTIONS ====
def dijkstra_dist(adj, s):
    # Success rate: 1/1

    import heapq
    INF = 10 ** 18
    n = len(adj)
    dist = [INF] * n
    dist[s] = 0
    heap = [(0, s)]
    while heap:
        (d, u) = heapq.heappop(heap)
        if d != dist[u]:
            continue
        for (v, w) in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(heap, (nd, v))
    return dist

def multi_source_bfs(neighbors, sources):
    # Success rate: 0.0/0
    n = len(neighbors)
    dist = [-1] * n
    q = [0] * n
    head = tail = 0
    for u in sources:
        if dist[u] < 0:
            dist[u] = 0
            q[tail] = u
            tail += 1
    while head < tail:
        u = q[head]
        head += 1
        du = dist[u] + 1
        for v in neighbors[u]:
            if dist[v] < 0:
                dist[v] = du
                q[tail] = v
                tail += 1
    return dist

def build_weighted_graph(n, edges):
    # Success rate: 1/1

    gp = [dict() for _ in range(n)]
    for (u, v, w) in edges:
        if v not in gp[u] or w < gp[u][v]:
            gp[u][v] = w
        if u not in gp[v] or w < gp[v][u]:
            gp[v][u] = w
    adj = [[] for _ in range(n)]
    for u in range(n):
        for (v, w) in gp[u].items():
            adj[u].append((v, w))
    return adj

def bfs_distance(adj, start):
    # Success rate: 2/2

    from collections import deque
    INF = float('inf')
    n = len(adj)
    dist = [INF] * n
    dist[start] = 0
    dq = deque([start])
    while dq:
        u = dq.popleft()
        for v in adj[u]:
            if dist[v] > dist[u] + 1:
                dist[v] = dist[u] + 1
                dq.append(v)
    return dist

def dijkstra(adj, src):
    # Success rate: 3/3

    from heapq import heappush, heappop
    INF = 10 ** 18
    n = len(adj)
    dist = [INF] * n
    parent = [-1] * n
    dist[src] = 0
    heap = [(0, src)]
    while heap:
        (d, u) = heappop(heap)
        if d > dist[u]:
            continue
        for (v, w) in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                parent[v] = u
                heappush(heap, (nd, v))
    return (dist, parent)

def build_adj_undirected(n, edges):
    # Success rate: 4/4

    adj = [[] for _ in range(n)]
    for (u, v, w) in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))
    return adj

def compute_min_reachable(adj, dist):
    # Success rate: 1/1

    n = len(adj)
    nodes = list(range(n))
    nodes.sort(key=lambda x: dist[x], reverse=True)
    ans = [0] * n
    for u in nodes:
        best = dist[u]
        for v in adj[u]:
            if dist[v] > dist[u]:
                best = min(best, ans[v])
            else:
                best = min(best, dist[v])
        ans[u] = best
    return ans


# ==== NEW HELPER FUNCTIONS ====
def bfs_dist(adj, start):
    from collections import deque
    n = len(adj)
    dist = [-1] * n
    dist[start] = 0
    dq = deque([start])
    while dq:
        u = dq.popleft()
        for v in adj[u]:
            if dist[v] < 0:
                dist[v] = dist[u] + 1
                dq.append(v)
    return dist

def topo_min(n, edges):
    from collections import deque
    indegree = [0] * n
    for u in range(n):
        for v in edges[u]:
            indegree[v] += 1
    dq = deque([u for u in range(n) if indegree[u] == 0])
    order = []
    while dq:
        u = dq.popleft()
        order.append(u)
        for v in edges[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                dq.append(v)
    if len(order) < n:
        return None
    container = list(range(n))
    for u in reversed(order):
        for v in edges[u]:
            if container[v] < container[u]:
                container[u] = container[v]
    return container

def reverse_edges(edges):
    n = len(edges)
    rev = [[] for _ in range(n)]
    for u in range(n):
        for v in edges[u]:
            rev[v].append(u)
    return rev

def dfs(adj, start, visited):
    stack = [start]
    visited[start] = True
    while stack:
        u = stack.pop()
        for v in adj[u]:
            if not visited[v]:
                visited[v] = True
                stack.append(v)

def kosaraju_scc(graph):
    n = len(graph)
    seen = [False] * n
    order = []
    # first pass: build finish order
    for u in range(n):
        if not seen[u]:
            stack = [(u, False)]
            while stack:
                v, post = stack.pop()
                if post:
                    order.append(v)
                else:
                    if seen[v]:
                        continue
                    seen[v] = True
                    stack.append((v, True))
                    for w in graph[v]:
                        if not seen[w]:
                            stack.append((w, False))
    # second pass on reversed graph
    rev = reverse_edges(graph)
    comp_id = [-1] * n
    cid = 0
    for u in reversed(order):
        if comp_id[u] < 0:
            stack = [u]
            comp_id[u] = cid
            while stack:
                v = stack.pop()
                for w in rev[v]:
                    if comp_id[w] < 0:
                        comp_id[w] = cid
                        stack.append(w)
            cid += 1
    return comp_id, cid


# ########################################
#
#  PROGRAM REFACTORINGS
#
# ########################################

# ########## PROGRAM: node_10:cc_python_10 ##########

from codebank import bfs_dist

def main():
    import sys
    input = sys.stdin.readline
    n, m, s, t = map(int, input().split())
    s -= 1; t -= 1
    graph = [set() for _ in range(n)]
    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1; v -= 1
        graph[u].add(v)
        graph[v].add(u)
    ds = bfs_dist(graph, s)
    dt = bfs_dist(graph, t)
    dist_st = ds[t]
    ans = 0
    for u in range(n):
        for v in range(u+1, n):
            if v not in graph[u] and min(ds[u] + dt[v], dt[u] + ds[v]) + 1 >= dist_st:
                ans += 1
    print(ans)

if __name__ == "__main__":
    main()

# ########## PROGRAM: node_20:cc_python_20 ##########

from codebank import kosaraju_scc, dfs

def main():
    import sys
    input = sys.stdin.readline
    n, m, s = map(int, input().split())
    s -= 1
    graph = [[] for _ in range(n)]
    for _ in range(m):
        u, v = map(int, input().split())
        graph[u-1].append(v-1)
    comp_id, comp_cnt = kosaraju_scc(graph)
    comp_graph = [set() for _ in range(comp_cnt)]
    for u in range(n):
        cu = comp_id[u]
        for v in graph[u]:
            cv = comp_id[v]
            if cu != cv:
                comp_graph[cu].add(cv)
    reachable = [False] * comp_cnt
    dfs(comp_graph, comp_id[s], reachable)
    indegree = [0] * comp_cnt
    for u in range(comp_cnt):
        if reachable[u]:
            continue
        for v in comp_graph[u]:
            if not reachable[v]:
                indegree[v] += 1
    ans = sum(1 for u in range(comp_cnt) if not reachable[u] and indegree[u] == 0)
    print(ans)

if __name__ == "__main__":
    main()

# ########## PROGRAM: node_8:cc_python_8 ##########

from codebank import topo_min, reverse_edges

def main():
    import sys
    input = sys.stdin.readline
    n, m = map(int, input().split())
    edges = [[] for _ in range(n)]
    for _ in range(m):
        u, v = map(int, input().split())
        edges[u-1].append(v-1)
    forward = topo_min(n, edges)
    if forward is None:
        print(-1)
        return
    backward = topo_min(n, reverse_edges(edges))
    container = [min(a, b) for a, b in zip(forward, backward)]
    res = sum(1 for i in range(n) if container[i] == i)
    s = ''.join('A' if container[i] == i else 'E' for i in range(n))
    print(res)
    print(s)

if __name__ == "__main__":
    main()
