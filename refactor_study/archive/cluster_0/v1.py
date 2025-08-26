# ########## LIBRARY HELPERS ##########

# ==== RETRIEVED HELPER FUNCTIONS (NONE) ====

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


# ########################################
#
#  PROGRAM REFACTORINGS
#
# ########################################

# ########## PROGRAM: node_13:cc_python_13 ##########

from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    n = int(input())
    if n % 2:
        print(-1)
        return
    edges = [tuple(int(x)-1 for x in input().split()) for _ in range(n-1)]
    adj = build_adj(n, edges)
    sz = [0]*n
    res = 0
    for u, p in iterative_postorder(adj):
        total = 1
        for v in adj[u]:
            if v != p:
                total += sz[v]
        sz[u] = total
        if p != -1 and total % 2 == 0:
            res += 1
    print(res)

if __name__ == "__main__":
    main()

# ########## PROGRAM: node_19:cc_python_19 ##########

from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    n = int(input())
    parents = [int(input()) for _ in range(n-1)]
    children = build_tree_children(n, parents)
    for v in range(1, n+1):
        if children[v]:
            leaves = sum(1 for u in children[v] if not children[u])
            if leaves < 3:
                print("No")
                return
    print("Yes")

if __name__ == "__main__":
    main()

# ########## PROGRAM: node_29:cc_python_29 ##########

from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    n = int(input())
    colors = list(map(int, input().split()))
    edges = [tuple(int(x)-1 for x in input().split()) for _ in range(n-1)]
    adj = build_adj(n, edges)
    total_red = colors.count(1)
    total_blue = colors.count(2)
    subtree = [[0, 0] for _ in range(n)]
    ans = 0
    for u, p in iterative_postorder(adj):
        r = 0; b = 0
        for v in adj[u]:
            if v != p:
                cr, cb = subtree[v]
                r += cr; b += cb
                if (cr == total_red and cb == 0) or (cb == total_blue and cr == 0):
                    ans += 1
        if colors[u] == 1:
            r += 1
        elif colors[u] == 2:
            b += 1
        subtree[u] = [r, b]
    print(ans)

if __name__ == "__main__":
    main()
