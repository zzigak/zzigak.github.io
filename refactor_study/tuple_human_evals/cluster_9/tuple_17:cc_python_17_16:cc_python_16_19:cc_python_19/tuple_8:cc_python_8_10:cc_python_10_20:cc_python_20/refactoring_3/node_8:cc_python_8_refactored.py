from codebank import *

def main():
    n, m = map(int, input().split())
    A = [tuple(map(int, input().split())) for _ in range(m)]
    edges_f = build_graph(n, A, False)
    cf = compute_reach_min(n, edges_f)
    if cf is None:
        print(-1)
        return
    edges_b = build_graph(n, A, True)
    cb = compute_reach_min(n, edges_b)
    container = [min(cf[i], cb[i]) for i in range(n)]
    res = sum(1 for i in range(n) if container[i] == i)
    s = ''.join('A' if container[i] == i else 'E' for i in range(n))
    print(res)
    print(s)

if __name__ == "__main__":
    main()