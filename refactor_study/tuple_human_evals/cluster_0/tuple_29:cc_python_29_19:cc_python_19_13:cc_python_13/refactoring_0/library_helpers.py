# ==== RETRIEVED HELPER FUNCTIONS (NONE) ====

# ==== NEW HELPER FUNCTIONS ====
import sys
def read_int():
    return int(sys.stdin.readline())
def read_ints():
    return list(map(int, sys.stdin.readline().split()))
def build_undirected_adj(n, edges):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    return adj
def post_order_traversal(adj, root=0):
    n = len(adj)
    parent = [-1]*n
    stack = [(root, -1, False)]
    order = []
    while stack:
        node, par, visited = stack.pop()
        if visited:
            order.append(node)
        else:
            stack.append((node, par, True))
            for nei in adj[node]:
                if nei != par:
                    parent[nei] = node
                    stack.append((nei, node, False))
    return order, parent
def count_nice_edges(adj, colors):
    total_red = colors.count(1)
    total_blue = colors.count(2)
    n = len(adj)
    cnt = [[0,0] for _ in range(n)]
    order, parent = post_order_traversal(adj, 0)
    ans = 0
    for u in order:
        if colors[u] == 1:
            cnt[u][0] += 1
        elif colors[u] == 2:
            cnt[u][1] += 1
        par = parent[u]
        if par != -1:
            r, b = cnt[u]
            if (r == total_red and b == 0) or (b == total_blue and r == 0):
                ans += 1
            cnt[par][0] += r
            cnt[par][1] += b
    return ans
def build_children(n, parents):
    children = [[] for _ in range(n)]
    for idx, p in enumerate(parents):
        children[p].append(idx+1)
    return children
def count_leaf_children(children, node):
    return sum(1 for ch in children[node] if not children[ch])
def count_even_cuts(adj):
    order, parent = post_order_traversal(adj, 0)
    n = len(adj)
    size = [1]*n
    cuts = 0
    for u in order:
        par = parent[u]
        if par != -1:
            if size[u] % 2 == 0:
                cuts += 1
            else:
                size[par] += size[u]
    return cuts
