from codebank import *

def main():
    import sys
    sys.setrecursionlimit(10**7)
    n,m=map(int,input().split())
    edges=[tuple(int(x)-1 for x in input().split()) for _ in range(m)]
    adj=build_adj(n,edges,True)
    fwd=compute_min_reachable(adj)
    if fwd is None:
        print(-1)
        return
    bwd=compute_min_reachable(reverse_adj(adj))
    cont=[min(fwd[i],bwd[i]) for i in range(n)]
    res=sum(1 for i in range(n) if cont[i]==i)
    print(res)
    print(''.join('A' if cont[i]==i else 'E' for i in range(n)))

if __name__=='__main__':
    main()