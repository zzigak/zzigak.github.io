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
def build_adj_list(n, edges, directed=False):
    adj = [[] for _ in range(n)]
    for (u, v) in edges:
        adj[u].append(v)
        if not directed:
            adj[v].append(u)
    return adj

# Selected because: after removing an edge, we need to find a leaf (an endpoint)
# of the resulting component; BFS farthest from the cut vertex always yields a leaf.
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

def build_adj_list(n, edges, directed=False):
    """
    Build an adjacency list for a graph with n nodes (0..n-1)
    edges: iterable of (u, v) pairs
    directed: if False, also adds edge (v, u)
    """
    adj = [[] for _ in range(n)]
    for (u, v) in edges:
        adj[u].append(v)
        if not directed:
            adj[v].append(u)
    return adj

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

def build_adj_list(n, edges, directed=False):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        if not directed:
            adj[v].append(u)
    return adj

def bfs_reachable(start, adj, banned=None):
    if banned is None: banned = set()
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

def dfs_cuts(x, parent, adj, visited, cuts):
    visited.add(x)
    cnt = 0
    for y in list(adj[x]):
        if y not in visited:
            keep = dfs_cuts(y, x, adj, visited, cuts)
            if keep:
                cnt += 1
                if cnt > 2:
                    cuts.append((x, y))
            else:
                cuts.append((x, y))
    if cnt < 2:
        return True
    if parent is not None:
        return False

def leaf(start, adj):
    x, prev = start, None
    while True:
        nxt = None
        for y in adj[x]:
            if y != prev:
                nxt = y
                break
        if nxt is None:
            break
        prev, x = x, nxt
    return x

def dfs_order(E):
    n = len(E)
    visited = [False]*n
    order = []
    for u in range(n):
        if not visited[u]:
            stack = [(u, 0)]
            while stack:
                node, st = stack.pop()
                if st == 0:
                    if visited[node]: continue
                    visited[node] = True
                    stack.append((node, 1))
                    for v in E[node]:
                        if not visited[v]:
                            stack.append((v, 0))
                else:
                    order.append(node)
    return order

def kosaraju_scc(E):
    order = dfs_order(E)
    n = len(E)
    RE = [[] for _ in range(n)]
    for u in range(n):
        for v in E[u]:
            RE[v].append(u)
    comp = [-1]*n
    cid = 0
    for u in reversed(order):
        if comp[u] == -1:
            stack = [u]
            comp[u] = cid
            while stack:
                x = stack.pop()
                for y in RE[x]:
                    if comp[y] == -1:
                        comp[y] = cid
                        stack.append(y)
            cid += 1
    return comp, cid
