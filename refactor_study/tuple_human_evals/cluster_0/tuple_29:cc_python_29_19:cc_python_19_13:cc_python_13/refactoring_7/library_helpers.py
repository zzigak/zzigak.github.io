# ==== RETRIEVED HELPER FUNCTIONS (NONE) ====

# ==== NEW HELPER FUNCTIONS ====
def read_int():
    return int(input())

def read_ints():
    return list(map(int, input().split()))

def build_adj_list(n):
    adj = [[] for _ in range(n)]
    for _ in range(n - 1):
        u, v = read_ints()
        u -= 1; v -= 1
        adj[u].append(v)
        adj[v].append(u)
    return adj

def get_parent_and_postorder(adj, root=0):
    n = len(adj)
    parent = [-1] * n
    order = [root]
    for v in order:
        for u in adj[v]:
            if u != parent[v]:
                parent[u] = v
                order.append(u)
    return parent, order[::-1]

def build_children_from_parents(n):
    children = [[] for _ in range(n)]
    for i in range(1, n):
        p = read_int() - 1
        children[p].append(i)
    return children

def is_spruce(children):
    for v, ch in enumerate(children):
        if ch:
            cnt = 0
            for c in ch:
                if not children[c]:
                    cnt += 1
            if cnt < 3:
                return False
    return True
