from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    n, m = map(int, input().split())
    edges = [tuple(map(int, input().split())) for _ in range(m)]
    adj_f = build_graph(n, edges, False)
    lab_f = compute_min_label(adj_f)
    if lab_f is None:
        print(-1)
        return
    adj_b = build_graph(n, edges, True)
    lab_b = compute_min_label(adj_b)
    if lab_b is None:
        print(-1)
        return
    lab = [min(lab_f[i], lab_b[i]) for i in range(n)]
    res = sum(1 for i in range(n) if lab[i] == i)
    s = ''.join('A' if lab[i] == i else 'E' for i in range(n))
    print(res)
    print(s)

if __name__ == "__main__":
    main()