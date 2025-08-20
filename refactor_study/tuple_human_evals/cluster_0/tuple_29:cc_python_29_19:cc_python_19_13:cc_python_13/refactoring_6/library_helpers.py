# ==== RETRIEVED HELPER FUNCTIONS (NONE) ====

# ==== NEW HELPER FUNCTIONS ====
def build_adj_list(n, edges, directed=False):
    adj=[[] for _ in range(n)]
    for u,v in edges:
        adj[u].append(v)
        if not directed: adj[v].append(u)
    return adj

def dfs_subtree_sizes(node, adj, parent, sizes):
    total=1
    for nei in adj[node]:
        if nei!=parent:
            total+=dfs_subtree_sizes(nei, adj, node, sizes)
    sizes[node]=total
    return total

def dfs_color_count(node, adj, parent, colors, total_red, total_blue, counts, nice_edges):
    r = 1 if colors[node]==1 else 0
    b = 1 if colors[node]==2 else 0
    for nei in adj[node]:
        if nei!=parent:
            cr, cb = dfs_color_count(nei, adj, node, colors, total_red, total_blue, counts, nice_edges)
            if (cr==total_red and cb==0) or (cb==total_blue and cr==0):
                nice_edges[0]+=1
            r += cr; b += cb
    counts[node]=(r,b)
    return r, b

def build_children(n, parents):
    children=[[] for _ in range(n)]
    for i,p in enumerate(parents, start=1):
        children[p].append(i)
    return children
