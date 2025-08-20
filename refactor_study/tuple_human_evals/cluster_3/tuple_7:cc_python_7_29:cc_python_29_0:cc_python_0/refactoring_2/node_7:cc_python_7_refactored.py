from codebank import *

def main():
    n = int(input())
    # read colors a_i: 1 for white, 0 for black
    a = read_ints()
    # map to +1 / -1
    val = [1 if c == 1 else -1 for c in a]
    adj = read_tree(n)
    dp, par, order = tree_dp_down(adj, 0, val)
    ans = tree_reroot(adj, 0, dp, par, order)
    print(*ans)

if __name__ == "__main__":
    main()