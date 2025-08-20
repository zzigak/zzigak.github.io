# ########## LIBRARY HELPERS ##########

# ==== RETRIEVED HELPER FUNCTIONS ====
def parorder(adj, root):
    # Success rate: 1/1

    par = [0] * len(adj)
    par[root] = -1
    stack = [root]
    order = []
    visited = {root}
    while stack:
        u = stack.pop()
        order.append(u)
        for v in adj[u]:
            if v not in visited:
                visited.add(v)
                par[v] = u
                stack.append(v)
    return (par, order)

def read_ints():
    # Success rate: 3/3

    return map(int, input().split())

def read_tree(n, offset=0):
    # Success rate: 3/3

    adj = [[] for _ in range(n + (1 if offset else 0))]
    for _ in range(n - 1):
        (u, v) = read_ints()
        if offset == 0:
            u -= 1
            v -= 1
        adj[u].append(v)
        adj[v].append(u)
    return adj

def get_children(par):
    # Success rate: 1/1

    children = [[] for _ in par]
    for (u, p) in enumerate(par):
        if p >= 0:
            children[p].append(u)
    return children


# ==== NEW HELPER FUNCTIONS ====


# ########################################
#
#  PROGRAM REFACTORINGS
#
# ########################################

# ########## PROGRAM: node_0:cc_python_0 ##########

from codebank import read_ints

def main():
    n = int(input())
    b = list(map(int, input().split()))
    a = list(map(int, input().split()))
    x = [0] * (n + 1)
    k = [0] * (n + 1)
    for i in range(2, n + 1):
        xi, ki = read_ints()
        x[i] = xi
        k[i] = ki
    diff = [0] * (n + 1)
    for i in range(1, n + 1):
        diff[i] = b[i - 1] - a[i - 1]
    for i in range(n, 1, -1):
        p = x[i]
        if diff[i] >= 0:
            diff[p] += diff[i]
        else:
            diff[p] += diff[i] * k[i]
    print("YES" if diff[1] >= 0 else "NO")

if __name__ == "__main__":
    main()

# ########## PROGRAM: node_29:cc_python_29 ##########

from codebank import *
def main():
    n = int(input())
    tree = read_tree(n, offset=1)
    v = list(map(int, input().split()))
    par, order = parorder(tree, 1)
    children = get_children(par)
    pos = [0] * (n + 1); neg = [0] * (n + 1)
    for u in reversed(order):
        for w in children[u]:
            if pos[w] > pos[u]: pos[u] = pos[w]
            if neg[w] > neg[u]: neg[u] = neg[w]
        cur = v[u - 1] + pos[u] - neg[u]
        if cur > 0:
            neg[u] += cur
        else:
            pos[u] += -cur
    print(pos[1] + neg[1])
if __name__ == "__main__":
    main()

# ########## PROGRAM: node_7:cc_python_7 ##########

from codebank import read_ints, read_tree, parorder, get_children

def main():
    n = int(input())
    a = list(map(int, input().split()))
    weight = [0] + [1 if ai else -1 for ai in a]
    tree = read_tree(n, offset=1)
    par, order = parorder(tree, 1)
    children = get_children(par)
    dp = [0] * (n + 1)
    for u in reversed(order):
        tot = 0
        for v in children[u]:
            tot += max(dp[v], 0)
        dp[u] = weight[u] + tot
    res = [0] * (n + 1)
    res[1] = dp[1]
    for u in order[1:]:
        p = par[u]
        res[u] = dp[u] + max(res[p] - max(dp[u], 0), 0)
    print(*res[1:])

if __name__ == "__main__":
    main()
