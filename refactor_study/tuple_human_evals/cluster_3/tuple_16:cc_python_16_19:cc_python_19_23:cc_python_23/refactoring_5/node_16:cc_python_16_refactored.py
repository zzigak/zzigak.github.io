from codebank import *

def main():
    n, k = map(int, input().split())
    adj = read_tree(n)
    par, order = parorder(adj, 0)
    depth = compute_depth(par, order)
    children = get_children(par)
    size = compute_subtree_sizes(children, order)
    diffs = [size[u] - depth[u] for u in range(n)]
    diffs.sort(reverse=True)
    print(sum(diffs[:n-k]))

if __name__ == "__main__":
    main()