from codebank import *
import sys

def main():
    input = sys.stdin.readline
    n, m = map(int, input().split())
    edges = [tuple(map(int, input().split())) for _ in range(m)]
    adj_f = build_directed_graph(n, edges)
    order_f = topological_sort(adj_f)
    if order_f is None:
        print(-1)
        return
    cont_f = propagate_min_label(adj_f, order_f)
    adj_b = build_directed_graph(n, edges, True)
    order_b = topological_sort(adj_b)
    cont_b = propagate_min_label(adj_b, order_b) if order_b is not None else [0]*n
    container = [min(cont_f[i], cont_b[i]) for i in range(n)]
    res = sum(1 for i in range(n) if container[i] == i)
    s = ''.join('A' if container[i] == i else 'E' for i in range(n))
    print(res)
    print(s)

if __name__ == "__main__":
    main()