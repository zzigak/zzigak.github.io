# ########## LIBRARY HELPERS ##########

# ==== RETRIEVED HELPER FUNCTIONS ====
def parorder(adj, root):
    # Success rate: 6/6

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
    # Success rate: 9/9

    return map(int, input().split())

def read_tree(n, offset=0):
    # Success rate: 7/7

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
    # Success rate: 5/5

    children = [[] for _ in par]
    for (u, p) in enumerate(par):
        if p >= 0:
            children[p].append(u)
    return children


# ==== NEW HELPER FUNCTIONS ====

def compute_par_depth_order(adj,root):
    par=[-1]*len(adj)
    depth=[0]*len(adj)
    order=[]
    stack=[root]
    while stack:
        u=stack.pop()
        order.append(u)
        for v in adj[u]:
            if v==par[u]: continue
            par[v]=u
            depth[v]=depth[u]+1
            stack.append(v)
    return par,depth,order

def compute_size_depth_scores(adj,root=0):
    par,depth,order=compute_par_depth_order(adj,root)
    size=[0]*len(adj)
    for u in reversed(order):
        for v in adj[u]:
            if par[u]==v: continue
            size[u]+=size[v]+1
    return [size[i]-depth[i] for i in range(len(adj))]

def max_beauty(L,R,adj,root=0):
    par,order=parorder(adj,root)
    dp=[[0,0] for _ in range(len(adj))]
    for u in reversed(order):
        v=par[u]
        if v<0: continue
        Lu,Ru=L[u],R[u]; Lv,Rv=L[v],R[v]
        zero=max(dp[u][0]+abs(Lv-Lu),dp[u][1]+abs(Lv-Ru))
        one =max(dp[u][0]+abs(Rv-Lu),dp[u][1]+abs(Rv-Ru))
        dp[v][0]+=zero; dp[v][1]+=one
    return max(dp[root])

def merge_dp(dp_v,dp_nv,K,mod=998244353):
    new_len=max(len(dp_v),len(dp_nv)+1)
    res=[0]*new_len
    for i,val_v in enumerate(dp_v):
        if not val_v: continue
        for j,val_nv in enumerate(dp_nv):
            prod=val_v*val_nv
            if i+j+1<=K:
                idx=max(j+1,i)
                res[idx]=(res[idx]+prod)%mod
            res[i]=(res[i]+prod)%mod
    return res

def count_valid_edge_sets(adj,K,root=0,mod=998244353):
    par,order=parorder(adj,root)
    dp=[[1] for _ in range(len(adj))]
    for u in reversed(order):
        for v in adj[u]:
            if v==par[u]: continue
            dp[u]=merge_dp(dp[u],dp[v],K,mod)
    return sum(dp[root][:K+1])%mod


# ########################################
#
#  PROGRAM REFACTORINGS
#
# ########################################

# ########## PROGRAM: node_16:cc_python_16 ##########

from codebank import read_tree, compute_size_depth_scores

def main():
    import sys
    input=sys.stdin.readline
    n,k=map(int,input().split())
    adj=read_tree(n,offset=1)
    scores=compute_size_depth_scores(adj,root=1)[1:]
    scores.sort(reverse=True)
    print(sum(scores[:n-k]))

if __name__=="__main__":
    main()

# ########## PROGRAM: node_19:cc_python_19 ##########

from codebank import read_tree, max_beauty

def main():
    import sys
    input=sys.stdin.readline
    t=int(input())
    for _ in range(t):
        n=int(input())
        L=[]; R=[]
        for _ in range(n):
            l,r=map(int,input().split())
            L.append(l); R.append(r)
        adj=read_tree(n,offset=0)
        print(max_beauty(L,R,adj,root=0))

if __name__=="__main__":
    main()

# ########## PROGRAM: node_23:cc_python_23 ##########

from codebank import read_tree, count_valid_edge_sets

def main():
    import sys
    input=sys.stdin.readline
    n,K=map(int,input().split())
    adj=read_tree(n,offset=0)
    print(count_valid_edge_sets(adj,K,root=0))

if __name__=="__main__":
    main()
