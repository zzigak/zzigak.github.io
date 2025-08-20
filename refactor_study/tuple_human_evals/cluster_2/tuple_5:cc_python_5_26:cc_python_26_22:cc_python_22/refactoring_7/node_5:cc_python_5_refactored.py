from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    n, m = map(int, input().split())
    color_edges = {}
    for _ in range(m):
        u, v, c = map(int, input().split())
        u -= 1; v -= 1
        color_edges.setdefault(c, []).append((u, v))
    # build per‐color adjacency lists
    color_adj = {c: build_adj_list(n, edges) for c, edges in color_edges.items()}
    q = int(input())
    for _ in range(q):
        u, v = map(int, input().split())
        u -= 1; v -= 1
        cnt = 0
        for adj in color_adj.values():
            if v in bfs_reachable(u, [], adj):
                cnt += 1
        print(cnt)

if __name__ == "__main__":
    main()