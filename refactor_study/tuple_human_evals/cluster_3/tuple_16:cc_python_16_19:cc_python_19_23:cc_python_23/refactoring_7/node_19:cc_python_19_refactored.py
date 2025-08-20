from codebank import *
import sys
input = sys.stdin.buffer.readline

def main():
    t = int(input())
    for _ in range(t):
        n = int(input())
        L = [0]*n
        R = [0]*n
        for i in range(n):
            L[i], R[i] = map(int, input().split())
        adj = read_tree(n)
        ans = compute_beauty(L, R, adj, root=0)
        print(ans)

if __name__ == "__main__":
    main()