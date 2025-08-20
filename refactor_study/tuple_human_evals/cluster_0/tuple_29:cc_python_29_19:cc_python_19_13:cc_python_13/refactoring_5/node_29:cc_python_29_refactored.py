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