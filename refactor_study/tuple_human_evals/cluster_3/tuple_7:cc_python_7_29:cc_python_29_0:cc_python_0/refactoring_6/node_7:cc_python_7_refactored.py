from codebank import *
import sys
def main():
    sys.setrecursionlimit(10**7)
    n=int(input())
    c=[1 if a==1 else -1 for a in read_ints()]
    adj=[[] for _ in range(n)]
    for _ in range(n-1):
        u,v=read_ints();u-=1;v-=1
        adj[u].append(v);adj[v].append(u)
    par,order=parorder(adj,0)
    children=get_children(par)
    dp=[0]*n
    for u in reversed(order):
        s=c[u]
        for v in children[u]:
            if dp[v]>0: s+=dp[v]
        dp[u]=s
    ans=[0]*n
    ans[0]=dp[0]
    for u in order[1:]:
        p=par[u]
        contrib=dp[u] if dp[u]>0 else 0
        ans[u]=dp[u]+max(ans[p]-contrib,0)
    print(*ans)

if __name__=="__main__":
    main()