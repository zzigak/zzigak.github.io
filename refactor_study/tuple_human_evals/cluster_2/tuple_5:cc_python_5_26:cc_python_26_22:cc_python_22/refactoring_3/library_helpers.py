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
    visited = set(banned)|{start}
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
    return far, dist

def dfs_removals(x, parent, adj, removes, root):
    count_keep = 0
    for y in list(adj[x]):
        if y == parent: continue
        if dfs_removals(y, x, adj, removes, root):
            count_keep += 1
            if count_keep > 2:
                removes.append((x, y))
        else:
            removes.append((x, y))
    return count_keep < 2

def find_leaf(start, adj):
    prev = -1
    curr = start
    while True:
        nxt = None
        for y in adj[curr]:
            if y != prev:
                nxt = y
                break
        if nxt is None:
            return curr
        prev, curr = curr, nxt

def scc_indeg_zero(E):
    n = len(E)
    iE = [[] for _ in range(n)]
    for i, es in enumerate(E):
        for j in es:
            iE[j].append(i)
    order = []
    done = [0]*n  # 0->enter,1->visited,2->exit
    for i0 in range(n):
        if done[i0]: continue
        stack = [~i0, i0]
        while stack:
            i = stack.pop()
            if i < 0:
                if done[~i]==2: continue
                done[~i]=2
                order.append(~i)
            else:
                if done[i]: continue
                done[i]=1
                for j in E[i]:
                    if not done[j]:
                        stack.append(~j); stack.append(j)
    done = [0]*n
    comp_id = [0]*n
    cid = 0
    SCCs = []
    for i0 in reversed(order):
        if done[i0]: continue
        cid += 1
        stack = [~i0, i0]
        comp = []
        while stack:
            i = stack.pop()
            if i < 0:
                if done[~i]==2: continue
                done[~i]=2
                comp.append(~i)
                comp_id[~i] = cid-1
            else:
                if done[i]: continue
                done[i]=1
                for j in iE[i]:
                    if not done[j]:
                        stack.append(~j); stack.append(j)
        SCCs.append(comp)
    indeg_zero = [1]*cid
    for i, es in enumerate(E):
        for j in es:
            if comp_id[i]!=comp_id[j]:
                indeg_zero[comp_id[j]] = 0
    return indeg_zero
