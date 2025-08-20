from codebank import *

def main():
    n, k = read_ints()
    adj = read_tree(n)
    par, order = parorder(adj, 0)
    depth = compute_depths(par, order)
    sizes = subtree_sizes(par, order)
    profits = [(sizes[i] - 1) - depth[i] for i in range(n)]
    profits.sort(reverse=True)
    # choose n-k tourism cities
    print(sum(profits[:n-k]))

if __name__ == "__main__":
    main()