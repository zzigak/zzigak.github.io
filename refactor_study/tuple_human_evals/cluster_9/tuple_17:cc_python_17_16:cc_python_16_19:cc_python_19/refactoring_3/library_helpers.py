# ==== RETRIEVED HELPER FUNCTIONS (NONE) ====

# ==== NEW HELPER FUNCTIONS ====
def read_ints():
    return map(int, input().split())

def build_undirected_graph(n, edges):
    adj = {i: [] for i in range(n)}
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))
    return adj

def dijkstra_path(adj, n, src, dest):
    import heapq
    INF = 10**18
    dist = [INF] * n
    parent = [-1] * n
    dist[src] = 0
    heap = [(0, src)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        if u == dest:
            break
        for v, w in adj.get(u, []):
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                parent[v] = u
                heapq.heappush(heap, (nd, v))
    if dist[dest] == INF:
        return []
    path = []
    cur = dest
    while cur != -1:
        path.append(cur + 1)
        cur = parent[cur]
    return path[::-1]

def two_step_shortest(adj, n, src):
    import heapq
    INF = 10**30
    dist = [INF] * n
    dist[src] = 0
    heap = [(0, src)]
    while heap:
        d, v = heapq.heappop(heap)
        if d > dist[v]:
            continue
        for u, w1 in adj.get(v, []):
            for x, w2 in adj.get(u, []):
                nd = d + (w1 + w2) ** 2
                if nd < dist[x]:
                    dist[x] = nd
                    heapq.heappush(heap, (nd, x))
    return dist

def build_rev_graph_and_sources(a):
    n = len(a)
    adj_rev = [[] for _ in range(n)]
    ans = [-1] * n
    sources = []
    for i, x in enumerate(a):
        for j in (i - x, i + x):
            if 0 <= j < n:
                if (a[j] % 2) != (x % 2):
                    if ans[i] == -1:
                        ans[i] = 1
                        sources.append(i)
                else:
                    adj_rev[j].append(i)
    return adj_rev, sources, ans

def multi_source_bfs(adj_rev, sources, ans):
    from collections import deque
    dq = deque(sources)
    while dq:
        v = dq.popleft()
        for u in adj_rev[v]:
            if ans[u] == -1:
                ans[u] = ans[v] + 1
                dq.append(u)
    return ans
