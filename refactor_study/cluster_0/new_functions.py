# ==== NEW HELPER FUNCTIONS ====
def build_adj(n, edges):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    return adj

def iterative_postorder(adj, root=0):
    OBS, POST = 0, 1
    stack = [(OBS, root, -1)]
    while stack:
        state, u, p = stack.pop()
        if state == OBS:
            stack.append((POST, u, p))
            for v in adj[u]:
                if v != p:
                    stack.append((OBS, v, u))
        else:
            yield u, p

def build_tree_children(n, parents):
    children = [[] for _ in range(n+1)]
    for i, p in enumerate(parents, start=2):
        children[p].append(i)
    return children