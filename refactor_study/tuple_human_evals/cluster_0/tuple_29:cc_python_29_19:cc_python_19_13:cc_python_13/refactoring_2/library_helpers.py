# ==== RETRIEVED HELPER FUNCTIONS (NONE) ====

# ==== NEW HELPER FUNCTIONS ====
def build_graph(n, edges, undirected=True):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        if undirected:
            adj[v].append(u)
    return adj

def dfs_parent_order(root, adj):
    parent = [-1] * len(adj)
    order = []
    stack = [root]
    while stack:
        node = stack.pop()
        order.append(node)
        for nei in adj[node]:
            if nei != parent[node]:
                parent[nei] = node
                stack.append(nei)
    return parent, order

def compute_subtree_counts(order, parent, node_values, num_values):
    n = len(order)
    counts = [[0]*num_values for _ in range(n)]
    for node in reversed(order):
        val = node_values[node]
        if val is not None:
            counts[node][val] += 1
        p = parent[node]
        if p != -1:
            for i in range(num_values):
                counts[p][i] += counts[node][i]
    return counts

def count_nice_edges(parent, counts, total_counts):
    ans = 0
    for node, p in enumerate(parent):
        if p == -1:
            continue
        c = counts[node]
        if (c[0] == total_counts[0] and c[1] == 0) or \
           (c[1] == total_counts[1] and c[0] == 0):
            ans += 1
    return ans

def compute_subtree_sizes(order, parent):
    sizes = [1] * len(order)
    for node in reversed(order):
        p = parent[node]
        if p != -1:
            sizes[p] += sizes[node]
    return sizes

def max_even_cuts(sizes, parent):
    return sum(1 for node, p in enumerate(parent) if p != -1 and sizes[node] % 2 == 0)
