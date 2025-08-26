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

def dfs_prune(x, parent, adj, removals):
    """
    DFS to decide which child edges to remove so each node keeps at most 2 children.
    Returns True if this subtree can attach to parent (kept), else False.
    """
    cnt = 0
    for y in adj[x]:
        if y == parent:
            continue
        keep = dfs_prune(y, x, adj, removals)
        if keep:
            cnt += 1
            if cnt > 2:
                removals.append((x, y))
        else:
            removals.append((x, y))
    return cnt < 2

def find_removal_edges(adj):
    """
    Returns list of edges (u,v) to remove to make tree a bamboo.
    Nodes are 0-based; root is 0.
    """
    removals = []
    dfs_prune(0, -1, adj, removals)
    return removals

def remove_edges(adj, edges):
    """
    Remove each edge (u,v) from adj in both directions.
    """
    for u, v in edges:
        adj[u].remove(v)
        adj[v].remove(u)

def find_leaf(start, adj):
    """
    Find a leaf node reachable from 'start' in a tree (0-based).
    """
    prev = -1
    curr = start
    while True:
        for nbr in adj[curr]:
            if nbr != prev:
                prev, curr = curr, nbr
                break
        else:
            return curr

def build_rewire_operations(removals, adj):
    """
    Given removal edges and the pruned tree adj,
    build list of operations (x1,y1,x2,y2) in 0-based.
    """
    ops = []
    leaf_curr = find_leaf(0, adj)
    for u, v in removals:
        new_leaf = find_leaf(v, adj)
        ops.append((u, v, leaf_curr, new_leaf))
        leaf_curr = find_leaf(new_leaf, adj)
    return ops

def scc_ciE(E):
    """
    Given directed graph E as adjacency list, compute SCCs and return list ciE
    where ciE[c] = 1 if SCC c has no incoming edges from other SCCs, else 0.
    """
    n = len(E)
    # build inverse graph
    iE = [[] for _ in range(n)]
    for u, nbrs in enumerate(E):
        for v in nbrs:
            iE[v].append(u)
    # first pass: order by finish time
    done = [0]*n  # 0=unseen,1=in stack,2=processed
    order = []
    for i in range(n):
        if done[i]:
            continue
        stk = [~i, i]
        while stk:
            x = stk.pop()
            if x < 0:
                u = ~x
                if done[u] == 2:
                    continue
                done[u] = 2
                order.append(u)
            else:
                if done[x]:
                    continue
                done[x] = 1
                stk.append(~x)
                for y in E[x]:
                    if not done[y]:
                        stk.append(~y)
                        stk.append(y)
    # second pass: assign components
    comp_id = [0]*n
    done = [0]*n
    cid = 0
    for u in reversed(order):
        if done[u]:
            continue
        stk = [~u, u]
        while stk:
            x = stk.pop()
            if x < 0:
                v = ~x
                if done[v] == 2:
                    continue
                done[v] = 2
                comp_id[v] = cid
            else:
                if done[x]:
                    continue
                done[x] = 1
                stk.append(~x)
                for y in iE[x]:
                    if not done[y]:
                        stk.append(~y)
                        stk.append(y)
        cid += 1
    # compute ciE
    ciE = [1]*cid
    for u, nbrs in enumerate(E):
        cu = comp_id[u]
        for v in nbrs:
            cv = comp_id[v]
            if cu != cv:
                ciE[cv] = 0
    return ciE


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
    N, M = map(int, input().split())
    grid = [input().rstrip() for _ in range(N)]
    cnts = list(map(int, input().split()))  # read and ignore
    # index sand blocks
    id_map = [[-1]*M for _ in range(N)]
    I = []
    for j in range(M):
        for i in range(N-1, -1, -1):
            if grid[i][j] == '#':
                id_map[i][j] = len(I)
                I.append((i, j))
            elif i < N-1:
                id_map[i][j] = id_map[i+1][j]
    su = len(I)
    E = [[] for _ in range(su)]
    for k, (i, j) in enumerate(I):
        if i+1 < N and id_map[i+1][j] >= 0:
            E[k].append(id_map[i+1][j])
        if i-1 >= 0 and grid[i-1][j] == '#':
            E[k].append(id_map[i-1][j])
        if j-1 >= 0 and id_map[i][j-1] >= 0:
            E[k].append(id_map[i][j-1])
        if j+1 < M and id_map[i][j+1] >= 0:
            E[k].append(id_map[i][j+1])
    ciE = scc_ciE(E)
    print(sum(ciE))

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
        edges = [tuple(map(int, input().split())) for _ in range(n-1)]
        # convert to 0-based and build tree
        edges0 = [(u-1, v-1) for u, v in edges]
        adj = build_adj_list(n, edges0)
        removals = find_removal_edges(adj)
        remove_edges(adj, removals)
        ops = build_rewire_operations(removals, adj)
        print(len(ops))
        for x, y, l, r in ops:
            # output 1-based
            print(x+1, y+1, l+1, r+1)

if __name__ == "__main__":
    main()

# ########## PROGRAM: node_5:cc_python_5 ##########

from codebank import *

def main():
    n, m = map(int, input().split())
    edges_by_color = {}
    for _ in range(m):
        u, v, c = map(int, input().split())
        edges_by_color.setdefault(c, []).append((u-1, v-1))
    graph = {c: build_adj_list(n, es) for c, es in edges_by_color.items()}
    q = int(input())
    for _ in range(q):
        u, v = map(int, input().split())
        u -= 1; v -= 1
        cnt = 0
        for adj in graph.values():
            if v in bfs_reachable(u, [], adj):
                cnt += 1
        print(cnt)

if __name__ == "__main__":
    main()
