from codebank import *
import sys

def main():
    input = sys.stdin.readline
    n = int(input())
    a = list(read_ints())
    rev_adj = [[] for _ in range(n)]
    sources = []
    for i, ai in enumerate(a):
        for j in (i - ai, i + ai):
            if 0 <= j < n:
                if (a[j] & 1) != (ai & 1):
                    sources.append(i)
                else:
                    rev_adj[j].append(i)
    dist = multi_source_bfs(n, rev_adj, sources)
    print(" ".join(str(d) for d in dist))

if __name__ == "__main__":
    main()