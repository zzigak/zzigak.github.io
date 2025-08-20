from codebank import *
import sys

def main():
    n, k = list(read_ints())
    adj = read_tree(n)
    par, depth, order = par_depth_order(adj, 0)
    sz = subtree_sizes(par, order)
    vals = sorted((sz[i] - depth[i] for i in range(n)), reverse=True)
    print(sum(vals[:n-k]))

if __name__ == "__main__":
    main()