from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    t = int(input())
    for _ in range(t):
        n = int(input())
        raw = [tuple(map(int, input().split())) for __ in range(n-1)]
        e = build_adj_list(n, [(u-1, v-1) for u, v in raw])
        g = []
        dfs_prune(0, -1, e, g)
        # remove edges marked for pruning
        for x, y in g:
            e[x].remove(y)
            e[y].remove(x)
        # compute endpoints (a,b) for each removed subtree
        ends = []
        for x, y in g:
            a, _ = bfs_farthest(y, e)
            b, _ = bfs_farthest(a, e)
            if a < b:
                ends.append((a, b))
            else:
                ends.append((b, a))
        ops = []
        for i, (x, y) in enumerate(g):
            if i == 0:
                x2 = x
                y2 = ends[0][0]
            else:
                prev_b = ends[i-1][1]
                x2 = prev_b
                y2 = ends[i][0]
            ops.append((x+1, y+1, x2+1, y2+1))
        print(len(ops))
        for x1, y1, x2, y2 in ops:
            print(x1, y1, x2, y2)

if __name__ == "__main__":
    main()