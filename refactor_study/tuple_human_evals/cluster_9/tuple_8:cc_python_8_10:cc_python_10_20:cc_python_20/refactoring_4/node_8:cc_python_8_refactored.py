from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    n, m = map(int, input().split())
    edges = [tuple(map(int, input().split())) for _ in range(m)]
    fwd = build_directed_graph(n, edges)
    cont_f = compute_min_reachable(fwd)
    if cont_f is None:
        print(-1)
        return
    bwd = build_directed_graph(n, edges, reversed=True)
    cont_b = compute_min_reachable(bwd)
    cont = [min(a, b) for a, b in zip(cont_f, cont_b)]
    res = sum(1 for i, x in enumerate(cont) if x == i)
    s = "".join("A" if cont[i] == i else "E" for i in range(n))
    print(res)
    print(s)

if __name__ == "__main__":
    main()