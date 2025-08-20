# ==== RETRIEVED HELPER FUNCTIONS (NONE) ====

# ==== NEW HELPER FUNCTIONS ====
import sys

def read_ints():
    return list(map(int, sys.stdin.readline().split()))

def build_adj_list(n, edges, undirected=True):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        if undirected:
            adj[v].append(u)
    return adj

def count_nice_edges(n, adj, colors):
    total_r = colors.count(1)
    total_b = colors.count(2)
    counts = [[0, 0] for _ in range(n)]
    result = 0
    OBS, CHK = 0, 1
    stack = [(OBS, 0, -1)]
    while stack:
        st, v, p = stack.pop()
        if st == OBS:
            stack.append((CHK, v, p))
            for nb in adj[v]:
                if nb != p:
                    stack.append((OBS, nb, v))
        else:
            r = b = 0
            for nb in adj[v]:
                if nb != p:
                    cr, cb = counts[nb]
                    if (cr == total_r and cb == 0) or (cb == total_b and cr == 0):
                        result += 1
                    r += cr; b += cb
            if colors[v] == 1:
                r += 1
            elif colors[v] == 2:
                b += 1
            counts[v][0] = r; counts[v][1] = b
    return result

def count_even_edges(n, adj):
    if n % 2 != 0:
        return -1
    sz = [0] * n
    res = 0
    OBS, CHK = 0, 1
    stack = [(OBS, 0, -1)]
    while stack:
        st, v, p = stack.pop()
        if st == OBS:
            stack.append((CHK, v, p))
            for nb in adj[v]:
                if nb != p:
                    stack.append((OBS, nb, v))
        else:
            total = 1
            for nb in adj[v]:
                if nb != p:
                    total += sz[nb]
                    if sz[nb] % 2 == 0:
                        res += 1
            sz[v] = total
    return res

def is_spruce(child):
    for kids in child:
        if kids:
            leaf_cnt = sum(1 for ch in kids if not child[ch])
            if leaf_cnt < 3:
                return False
    return True
