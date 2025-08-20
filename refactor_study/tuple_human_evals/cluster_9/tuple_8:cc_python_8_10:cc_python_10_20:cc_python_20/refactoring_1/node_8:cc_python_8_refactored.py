from codebank import *

def main():
    import sys
    data = sys.stdin.readline
    n, m = map(int, data().split())
    edges = []
    for _ in range(m):
        u, v = map(int, data().split())
        edges.append((u-1, v-1))
    g = build_dir_graph(n, edges)
    topo = get_topo_order(n, g)
    if topo is None:
        print(-1)
        return
    fwd = compute_min_dag(n, g, topo)
    gr = build_dir_graph(n, edges, rev=True)
    topo2 = get_topo_order(n, gr)
    back = compute_min_dag(n, gr, topo2)
    container = [fwd[i] if fwd[i] < back[i] else back[i] for i in range(n)]
    res = sum(1 for i in range(n) if container[i] == i)
    s = ''.join('A' if container[i] == i else 'E' for i in range(n))
    print(res)
    print(s)

if __name__ == "__main__":
    main()