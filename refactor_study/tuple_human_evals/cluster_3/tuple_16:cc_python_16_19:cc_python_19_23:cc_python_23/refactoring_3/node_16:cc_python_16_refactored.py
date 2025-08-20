from codebank import *

def main():
    n, k = read_ints()
    adj = read_tree(n)
    root = 0
    par, order = parorder(adj, root)
    depth = compute_depth(par, order)
    subtree = compute_subtree_sizes(par, order)
    benefits = [subtree[i] - 1 - depth[i] for i in range(n)]
    benefits.sort(reverse=True)
    # original picks n-k largest values
    print(sum(benefits[:n - k]))

if __name__ == "__main__":
    main()