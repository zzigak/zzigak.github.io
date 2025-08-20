from codebank import build_adj_list, bfs_reachable

def main():
    import sys
    input = sys.stdin.readline
    n, m = map(int, input().split())
    edges_by_color = {}
    for _ in range(m):
        u, v, c = map(int, input().split())
        edges_by_color.setdefault(c, []).append((u-1, v-1))
    adj_by_color = {c: build_adj_list(n, es) for c, es in edges_by_color.items()}
    q = int(input())
    for _ in range(q):
        u, v = map(int, input().split())
        u -= 1; v -= 1
        cnt = 0
        for adj in adj_by_color.values():
            if v in bfs_reachable(u, [], adj):
                cnt += 1
        print(cnt)

if __name__ == "__main__":
    main()