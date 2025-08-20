from codebank import read_tree, count_valid_edge_sets

def main():
    import sys
    input=sys.stdin.readline
    n,K=map(int,input().split())
    adj=read_tree(n,offset=0)
    print(count_valid_edge_sets(adj,K,root=0))

if __name__=="__main__":
    main()