from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    n, m = map(int, input().split())
    edges = [tuple(int(x)-1 for x in input().split()) for _ in range(m)]
    g = build_adj_directed(n, edges)
    cf = compute_min_reachable(g)
    if cf is None:
        print(-1)
        return
    gr = reverse_graph(g)
    cb = compute_min_reachable(gr)
    container = [min(cf[i], cb[i]) for i in range(n)]
    res = sum(1 for i in range(n) if container[i] == i)
    s = ''.join('A' if container[i] == i else 'E' for i in range(n))
    print(res)
    print(s)

if __name__ == "__main__":
    main()