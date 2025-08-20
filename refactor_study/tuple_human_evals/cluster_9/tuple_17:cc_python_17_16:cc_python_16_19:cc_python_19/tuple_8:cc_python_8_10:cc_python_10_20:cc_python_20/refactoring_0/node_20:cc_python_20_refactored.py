from codebank import *

def main():
    import sys
    sys.setrecursionlimit(10**7)
    n,m,s=map(int,input().split())
    s-=1
    edges=[tuple(int(x)-1 for x in input().split()) for _ in range(m)]
    adj=build_adj(n,edges,True)
    order=topo_sort(adj)
    dist=bfs(s,adj)
    seen=[d>=0 for d in dist]
    cnt=0
    for u in order:
        if not seen[u]:
            dist2=bfs(u,adj)
            for i,d in enumerate(dist2):
                if d>=0:
                    seen[i]=True
            cnt+=1
    print(cnt)

if __name__=='__main__':
    main()