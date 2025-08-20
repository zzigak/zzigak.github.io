from codebank import *

def main():
    import sys
    sys.setrecursionlimit(10000)
    n, m, s = map(int, sys.stdin.readline().split())
    s -= 1
    edges = []
    for _ in range(m):
        u, v = map(int, sys.stdin.readline().split())
        edges.append((u-1, v-1))
    comp, cnt = kosaraju_scc(n, edges)
    ans = count_new_roads_to_connect(n, edges, comp, cnt, s)
    print(ans)

if __name__ == "__main__":
    main()