# ########## LIBRARY HELPERS ##########

# ==== RETRIEVED HELPER FUNCTIONS ====

# Selected Helper Functions

from collections import deque

def build_adj_list(n, edges, directed=False):
    """
    Build an adjacency list for an undirected (by default) graph with n nodes (0-indexed)
    edges: list of (u, v) pairs
    """
    adj = [[] for _ in range(n)]
    for (u, v) in edges:
        adj[u].append(v)
        if not directed:
            adj[v].append(u)
    return adj
# Selected because: We need to construct, for each color, the subgraph adjacency list over which we'll test connectivity.

def bfs_reachable(start, banned, adj):
    """
    Return the set of nodes reachable from 'start' in the graph defined by adj,
    skipping any nodes in 'banned'.
    """
    visited = set(banned) | {start}
    q = deque([start])
    reach = set()
    while q:
        v = q.popleft()
        for u in adj[v]:
            if u not in visited:
                visited.add(u)
                reach.add(u)
                q.append(u)
    return reach
# Selected because: Provides a quick reachability test (via BFS) to check if, for a given color subgraph,
# vertex u_i can reach v_i (i.e. v_i ∈ bfs_reachable(u_i, [], adj_color)).


# Selected Helper Functions

from collections import deque

# Selected because: we need to build the tree's adjacency list efficiently.
def bfs_farthest(start, adj):
    n = len(adj)
    dist = [-1] * n
    dq = deque([start])
    dist[start] = 0
    while dq:
        v = dq.popleft()
        for u in adj[v]:
            if dist[u] < 0:
                dist[u] = dist[v] + 1
                dq.append(u)
    far = max(range(n), key=lambda i: dist[i])
    return (far, dist)


# Selected Helper Functions

from collections import deque

def dfs_comp(v, adj, comp, cid):
    """
    Depth-first search to label the connected component of node v
    comp: list of component IDs per node (0 = unvisited)
    cid: current component ID
    """
    comp[v] = cid
    for u in adj[v]:
        if comp[u] == 0:
            dfs_comp(u, adj, comp, cid)

def connected_components(adj):
    """
    Find connected components in an undirected graph given by adj list.
    Returns (comp, cid) where comp[v] is the component ID of v (1..cid)
    and cid is the total number of components.
    """
    n = len(adj)
    comp = [0] * n
    cid = 0
    for i in range(n):
        if comp[i] == 0:
            cid += 1
            dfs_comp(i, adj, comp, cid)
    return (comp, cid)


# ==== NEW HELPER FUNCTIONS ====
from collections import deque

def compute_scc_zero_incoming(E):
    """
    Given directed graph E as adjacency list, compute number of
    strongly connected components with zero incoming edges.
    """
    n = len(E)
    rev = [[] for _ in range(n)]
    for u, vs in enumerate(E):
        for v in vs:
            rev[v].append(u)
    visited = [False] * n
    order = []
    def dfs1(u):
        visited[u] = True
        for v in E[u]:
            if not visited[v]:
                dfs1(v)
        order.append(u)
    for i in range(n):
        if not visited[i]:
            dfs1(i)
    comp = [-1] * n
    cid = 0
    def dfs2(u):
        stack = [u]
        comp[u] = cid
        while stack:
            x = stack.pop()
            for v in rev[x]:
                if comp[v] == -1:
                    comp[v] = cid
                    stack.append(v)
    for u in reversed(order):
        if comp[u] == -1:
            dfs2(u)
            cid += 1
    has_in = [False] * cid
    for u in range(n):
        for v in E[u]:
            if comp[u] != comp[v]:
                has_in[comp[v]] = True
    return has_in.count(False)


# ########################################
#
#  PROGRAM REFACTORINGS
#
# ########################################

# ########## PROGRAM: node_22:cc_python_22 ##########

from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    n, m = map(int, input().split())
    grid = [input().rstrip('\n') for _ in range(n)]
    ZZ = [[-1] * m for _ in range(n)]
    I = []
    for j in range(m):
        for i in range(n-1, -1, -1):
            if grid[i][j] == '#':
                ZZ[i][j] = len(I)
                I.append((i, j))
            elif i < n-1:
                ZZ[i][j] = ZZ[i+1][j]
    su = len(I)
    E = [[] for _ in range(su)]
    for k, (i, j) in enumerate(I):
        if i+1 < n and ZZ[i+1][j] >= 0:
            E[k].append(ZZ[i+1][j])
        if i-1 >= 0 and grid[i-1][j] == '#':
            E[k].append(ZZ[i-1][j])
        if j-1 >= 0 and ZZ[i][j-1] >= 0:
            E[k].append(ZZ[i][j-1])
        if j+1 < m and ZZ[i][j+1] >= 0:
            E[k].append(ZZ[i][j+1])
    print(compute_scc_zero_incoming(E))

if __name__ == "__main__":
    main()

# ########## PROGRAM: node_26:cc_python_26 ##########

from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    t = int(input())
    for _ in range(t):
        n = int(input())
        raw = [tuple(map(int, input().split())) for __ in range(n-1)]
        e = build_adj_list(n, [(u-1, v-1) for u, v in raw])
        g = []
        dfs_prune(0, -1, e, g)
        # remove edges marked for pruning
        for x, y in g:
            e[x].remove(y)
            e[y].remove(x)
        # compute endpoints (a,b) for each removed subtree
        ends = []
        for x, y in g:
            a, _ = bfs_farthest(y, e)
            b, _ = bfs_farthest(a, e)
            if a < b:
                ends.append((a, b))
            else:
                ends.append((b, a))
        ops = []
        for i, (x, y) in enumerate(g):
            if i == 0:
                x2 = x
                y2 = ends[0][0]
            else:
                prev_b = ends[i-1][1]
                x2 = prev_b
                y2 = ends[i][0]
            ops.append((x+1, y+1, x2+1, y2+1))
        print(len(ops))
        for x1, y1, x2, y2 in ops:
            print(x1, y1, x2, y2)

if __name__ == "__main__":
    main()

# ########## PROGRAM: node_5:cc_python_5 ##########

from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    n, m = map(int, input().split())
    edges_per_color = {}
    for _ in range(m):
        u, v, c = map(int, input().split())
        u -= 1; v -= 1
        edges_per_color.setdefault(c, []).append((u, v))
    comp_per_color = {}
    for c, edges in edges_per_color.items():
        adj, _ = build_adj_list(n, edges), None
        comp, _ = connected_components(adj)
        comp_per_color[c] = comp
    q = int(input())
    for _ in range(q):
        u, v = map(int, input().split())
        u -= 1; v -= 1
        ans = 0
        for comp in comp_per_color.values():
            if comp[u] == comp[v]:
                ans += 1
        print(ans)

if __name__ == "__main__":
    main()
