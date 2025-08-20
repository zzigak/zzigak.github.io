from codebank import *

def main():
    import sys
    input=sys.stdin.readline
    n=int(input())
    colors=list(map(int,input().split()))
    edges=[tuple(map(lambda x:int(x)-1,input().split())) for _ in range(n-1)]
    adj=build_adj_list(n, edges)
    total_red=colors.count(1)
    total_blue=colors.count(2)
    counts=[(0,0) for _ in range(n)]
    nice_edges=[0]
    dfs_color_count(0, adj, -1, colors, total_red, total_blue, counts, nice_edges)
    print(nice_edges[0])

if __name__=="__main__":
    main()