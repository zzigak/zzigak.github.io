from codebank import topo_min, reverse_edges

def main():
    import sys
    input = sys.stdin.readline
    n, m = map(int, input().split())
    edges = [[] for _ in range(n)]
    for _ in range(m):
        u, v = map(int, input().split())
        edges[u-1].append(v-1)
    forward = topo_min(n, edges)
    if forward is None:
        print(-1)
        return
    backward = topo_min(n, reverse_edges(edges))
    container = [min(a, b) for a, b in zip(forward, backward)]
    res = sum(1 for i in range(n) if container[i] == i)
    s = ''.join('A' if container[i] == i else 'E' for i in range(n))
    print(res)
    print(s)

if __name__ == "__main__":
    main()