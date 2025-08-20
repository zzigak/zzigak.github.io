from codebank import *

def main():
    import sys
    data = sys.stdin.read().split()
    n = int(data[0])
    a = list(map(int, data[1:]))
    adj_rev, sources = build_reverse_graph(a)
    dist = multi_source_bfs(adj_rev, sources, n)
    INF = 10**30
    res = [str(-1 if d >= INF else d + 1) for d in dist]
    print(" ".join(res))

if __name__ == "__main__":
    main()