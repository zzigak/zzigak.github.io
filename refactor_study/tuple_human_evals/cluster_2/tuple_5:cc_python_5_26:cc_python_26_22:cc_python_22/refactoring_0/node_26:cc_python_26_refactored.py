from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    t = int(input())
    for _ in range(t):
        n = int(input())
        edges = [tuple(map(int, input().split())) for _ in range(n-1)]
        # convert to 0-based and build tree
        edges0 = [(u-1, v-1) for u, v in edges]
        adj = build_adj_list(n, edges0)
        removals = find_removal_edges(adj)
        remove_edges(adj, removals)
        ops = build_rewire_operations(removals, adj)
        print(len(ops))
        for x, y, l, r in ops:
            # output 1-based
            print(x+1, y+1, l+1, r+1)

if __name__ == "__main__":
    main()