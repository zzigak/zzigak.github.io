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