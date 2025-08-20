# ==== RETRIEVED HELPER FUNCTIONS (NONE) ====

# ==== NEW HELPER FUNCTIONS ====
def build_undirected_graph(n, edges):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v); adj[v].append(u)
    return adj

def root_tree(adj, root=0):
    n = len(adj); parent = [-1]*n; order = []; stack = [(root, -1, False)]
    while stack:
        node, par, vis = stack.pop()
        if vis:
            order.append(node)
        else:
            parent[node] = par; stack.append((node, par, True))
            for nei in adj[node]:
                if nei != par:
                    stack.append((nei, node, False))
    return order, parent

def aggregate_subtree(order, parent, init_vals, agg):
    res = [v[:] if isinstance(v, (list, tuple)) else v for v in init_vals]
    for node in order:
        par = parent[node]
        if par != -1:
            res[par] = agg(res[par], res[node])
    return res

def is_spruce(children):
    for chs in children:
        if chs:
            leaf_cnt = sum(1 for c in chs if not children[c])
            if leaf_cnt < 3:
                return False
    return True
