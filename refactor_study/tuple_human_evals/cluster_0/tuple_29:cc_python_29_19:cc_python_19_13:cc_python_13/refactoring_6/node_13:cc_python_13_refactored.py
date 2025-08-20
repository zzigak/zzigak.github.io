from codebank import *

def main():
    import sys
    input=sys.stdin.readline
    n=int(input())
    if n%2:
        print(-1); return
    edges=[tuple(map(lambda x:int(x)-1,input().split())) for _ in range(n-1)]
    adj=build_adj_list(n, edges)
    sizes=[0]*n
    dfs_subtree_sizes(0, adj, -1, sizes)
    print(sum(1 for i in range(1,n) if sizes[i]%2==0))

if __name__=="__main__":
    main()