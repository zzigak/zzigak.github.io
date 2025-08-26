# ########## LIBRARY HELPERS ##########

# ==== RETRIEVED HELPER FUNCTIONS (NONE) ====

# ==== NEW HELPER FUNCTIONS ====
def read_ints():
    return list(map(int, input().split()))

def build_undirected_weighted_graph(n, m):
    from collections import defaultdict
    adj = defaultdict(list)
    for _ in range(m):
        u, v, w = read_ints()
        u -= 1; v -= 1
        adj[u].append((v, w))
        adj[v].append((u, w))
    return adj

def dijkstra(adj, src, n):
    import heapq
    INF = 10**18
    dist = [INF]*n
    parent = [-1]*n
    visited = [False]*n
    dist[src] = 0
    heap = [(0, src)]
    while heap:
        d, u = heapq.heappop(heap)
        if visited[u]:
            continue
        visited[u] = True
        for v, w in adj.get(u, ()):
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                parent[v] = u
                heapq.heappush(heap, (nd, v))
    return dist, parent

def reconstruct_path(parent, dest):
    path = []
    while dest != -1:
        path.append(dest+1)
        dest = parent[dest]
    return path[::-1]

def dijkstra_special(e, n, src):
    import heapq
    INF = 10**18
    d = [INF]*n
    d[src] = 0
    heap = [(0, src)]
    while heap:
        cd, v = heapq.heappop(heap)
        if cd > d[v]:
            continue
        td = {}
        for u, w in e.get(v, ()):
            td[u] = w
        for u, w1 in td.items():
            for x, w2 in e.get(u, ()):
                cost = cd + (w1 + w2)**2
                if cost < d[x]:
                    d[x] = cost
                    heapq.heappush(heap, (cost, x))
    return d

def compute_min_moves_opposite_parity(a):
    from collections import deque
    n = len(a)
    go = [[] for _ in range(n)]
    ans = [-1]*n
    q = deque()
    for i, val in enumerate(a):
        for j in (i - val, i + val):
            if 0 <= j < n:
                if (a[j] % 2) != (val % 2):
                    ans[i] = 1
                    q.append(i)
                    break
                else:
                    go[j].append(i)
    while q:
        u = q.popleft()
        for v in go[u]:
            if ans[v] == -1:
                ans[v] = ans[u] + 1
                q.append(v)
    return ans


# ########################################
#
#  PROGRAM REFACTORINGS
#
# ########################################

# ########## PROGRAM: node_16:cc_python_16 ##########

from codebank import *

def main():
    n, m = read_ints()
    e = {}
    for _ in range(m):
        u, v, w = read_ints()
        u -= 1; v -= 1
        e.setdefault(u, []).append((v, w))
        e.setdefault(v, []).append((u, w))
    d = dijkstra_special(e, n, 0)
    print(" ".join(str(-1 if x >= 10**18 else int(x)) for x in d))

if __name__ == "__main__":
    main()

# ########## PROGRAM: node_17:cc_python_17 ##########

from codebank import *

def main():
    n, m = read_ints()
    adj = build_undirected_weighted_graph(n, m)
    dist, parent = dijkstra(adj, 0, n)
    if dist[n-1] >= 10**18:
        print(-1)
    else:
        path = reconstruct_path(parent, n-1)
        print(" ".join(map(str, path)))

if __name__ == "__main__":
    main()

# ########## PROGRAM: node_19:cc_python_19 ##########

from codebank import *

def main():
    n = int(input())
    a = read_ints()
    ans = compute_min_moves_opposite_parity(a)
    print(" ".join(map(str, ans)))

if __name__ == "__main__":
    main()
