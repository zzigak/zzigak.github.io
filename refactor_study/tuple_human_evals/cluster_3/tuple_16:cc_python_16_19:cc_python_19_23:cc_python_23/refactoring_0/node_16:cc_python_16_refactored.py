from codebank import read_tree, compute_size_depth_scores

def main():
    import sys
    input=sys.stdin.readline
    n,k=map(int,input().split())
    adj=read_tree(n,offset=1)
    scores=compute_size_depth_scores(adj,root=1)[1:]
    scores.sort(reverse=True)
    print(sum(scores[:n-k]))

if __name__=="__main__":
    main()