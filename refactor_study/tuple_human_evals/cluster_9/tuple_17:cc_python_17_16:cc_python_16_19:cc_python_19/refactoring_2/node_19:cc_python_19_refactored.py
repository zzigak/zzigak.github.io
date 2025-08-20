from codebank import *

def main():
    n = int(input())
    a = list(map(int, input().split()))
    adj_rev = [[] for _ in range(n)]
    sources = []
    for i, w in enumerate(a):
        for j in (i - w, i + w):
            if 0 <= j < n:
                if a[j] % 2 != w % 2:
                    sources.append((i, 1))
                else:
                    adj_rev[j].append(i)
    dist = multi_source_bfs(adj_rev, sources)
    print(" ".join(str(d) for d in dist))

if __name__ == "__main__":
    main()