from codebank import *

def main():
    import sys
    input=sys.stdin.readline
    n,m,s,t=map(int,input().split())
    s-=1; t-=1
    edges=[tuple(int(x)-1 for x in input().split()) for _ in range(m)]
    graph=build_adj(n,edges,False)
    graph=[set(nb) for nb in graph]
    ds=bfs(s,graph)
    dt=bfs(t,graph)
    ans=0
    for u in range(n):
        for v in range(u+1,n):
            if v not in graph[u] and min(ds[u]+dt[v],dt[u]+ds[v])+1>=ds[t]:
                ans+=1
    print(ans)

if __name__=='__main__':
    main()