from codebank import read_tree, max_beauty

def main():
    import sys
    input=sys.stdin.readline
    t=int(input())
    for _ in range(t):
        n=int(input())
        L=[]; R=[]
        for _ in range(n):
            l,r=map(int,input().split())
            L.append(l); R.append(r)
        adj=read_tree(n,offset=0)
        print(max_beauty(L,R,adj,root=0))

if __name__=="__main__":
    main()