# ########## LIBRARY HELPERS ##########

# ==== RETRIEVED HELPER FUNCTIONS (NONE) ====

# ==== NEW HELPER FUNCTIONS ====
def build_adj_list(n, edges):
    adj=[[] for _ in range(n)]
    for u,v in edges:
        adj[u].append(v); adj[v].append(u)
    return adj

def get_parent_children_postorder(adj, root=0):
    n=len(adj); parent=[-1]*n; children=[[] for _ in range(n)]; order=[]
    stack=[(root,-1,False)]
    while stack:
        node,p,vis=stack.pop()
        if vis:
            order.append(node)
        else:
            parent[node]=p
            stack.append((node,p,True))
            for nei in adj[node]:
                if nei!=p:
                    children[node].append(nei)
                    stack.append((nei,node,False))
    return parent, children, order

def compute_subtree_sizes(adj, root=0):
    parent, children, order = get_parent_children_postorder(adj, root)
    n=len(adj); sizes=[1]*n
    for node in order:
        for c in children[node]:
            sizes[node]+=sizes[c]
    return sizes, parent

def compute_nice_edges(adj, colors):
    parent, children, order = get_parent_children_postorder(adj)
    tr=sum(1 for c in colors if c==1); tb=sum(1 for c in colors if c==2)
    n=len(adj); cr=[0]*n; cb=[0]*n; nice=0
    for node in order:
        if colors[node]==1: cr[node]=1
        elif colors[node]==2: cb[node]=1
        for c in children[node]:
            r,c_b=cr[c],cb[c]
            if (r==0 or c_b==0) and (tr-r==0 or tb-c_b==0):
                nice+=1
            cr[node]+=r; cb[node]+=c_b
    return nice

def count_even_removal(adj):
    n=len(adj)
    sizes,_=compute_subtree_sizes(adj)
    if n%2: return -1
    return sum(1 for i in range(1,n) if sizes[i]%2==0)

def is_spruce(children):
    for i,ch in enumerate(children):
        if ch:
            if sum(1 for c in ch if not children[c])<3:
                return False
    return True


# ########################################
#
#  PROGRAM REFACTORINGS
#
# ########################################

# ########## PROGRAM: node_13:cc_python_13 ##########

from codebank import *

def main():
    import sys
    input=sys.stdin.readline
    n=int(input())
    edges=[tuple(v-1 for v in map(int,input().split())) for _ in range(n-1)]
    adj=build_adj_list(n,edges)
    print(count_even_removal(adj))

if __name__=="__main__":
    main()

# ########## PROGRAM: node_19:cc_python_19 ##########

from codebank import *

def main():
    import sys
    input=sys.stdin.readline
    n=int(input())
    children=[[] for _ in range(n)]
    for i in range(1,n):
        p=int(input())-1
        children[p].append(i)
    print("Yes" if is_spruce(children) else "No")

if __name__=="__main__":
    main()

# ########## PROGRAM: node_29:cc_python_29 ##########

from codebank import *

def main():
    import sys
    input=sys.stdin.readline
    n=int(input())
    colors=list(map(int,input().split()))
    edges=[tuple(v-1 for v in map(int,input().split())) for _ in range(n-1)]
    adj=build_adj_list(n,edges)
    print(compute_nice_edges(adj,colors))

if __name__=="__main__":
    main()
