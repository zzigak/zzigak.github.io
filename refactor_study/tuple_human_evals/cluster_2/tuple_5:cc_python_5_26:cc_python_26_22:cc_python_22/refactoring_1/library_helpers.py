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

def bfs_reachable(start, banned, adj):
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

def dfs_comp(v, adj, comp, cid):
    comp[v] = cid
    for u in adj[v]:
        if comp[u] == 0:
            dfs_comp(u, adj, comp, cid)

def connected_components(adj):
    n = len(adj)
    comp = [0]*n
    cid = 0
    for i in range(n):
        if comp[i] == 0:
            cid += 1
            dfs_comp(i, adj, comp, cid)
    return comp, cid

def bfs_farthest(start, adj):
    n = len(adj)
    dist = [-1]*n
    dq = deque([start])
    dist[start] = 0
    while dq:
        v = dq.popleft()
        for u in adj[v]:
            if dist[u] < 0:
                dist[u] = dist[v] + 1
                dq.append(u)
    far = max(range(n), key=lambda i: dist[i])
    return far

def mark_bad_edges(u, parent, adj, bad):
    cnt = 0
    for v in adj[u]:
        if v == parent:
            continue
        if mark_bad_edges(v, u, adj, bad):
            cnt += 1
            if cnt > 2:
                bad.append((u, v))
        else:
            bad.append((u, v))
    return cnt < 2

def dfs1(u, E, visited, order):
    visited[u] = True
    for v in E[u]:
        if not visited[v]:
            dfs1(v, E, visited, order)
    order.append(u)

def dfs2(u, iE, comp_id, label):
    comp_id[u] = label
    for v in iE[u]:
        if comp_id[v] < 0:
            dfs2(v, iE, comp_id, label)

def scc(E):
    n = len(E)
    iE = [[] for _ in range(n)]
    for i, es in enumerate(E):
        for v in es:
            iE[v].append(i)
    visited = [False]*n
    order = []
    for i in range(n):
        if not visited[i]:
            dfs1(i, E, visited, order)
    comp_id = [-1]*n
    label = 0
    for u in reversed(order):
        if comp_id[u] < 0:
            dfs2(u, iE, comp_id, label)
            label += 1
    ciE = [1]*label
    for u in range(n):
        for v in E[u]:
            if comp_id[u] != comp_id[v]:
                ciE[comp_id[v]] = 0
    return ciE
