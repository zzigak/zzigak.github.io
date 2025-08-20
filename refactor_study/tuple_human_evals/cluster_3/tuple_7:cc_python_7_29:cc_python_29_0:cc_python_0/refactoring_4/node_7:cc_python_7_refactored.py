from codebank import *

def main():
    n = int(input())
    a = list(map(int, input().split()))
    adj = read_tree(n)
    par, order = parorder(adj)
    children = get_children(par)
    dp = compute_initial_dp(order, children, a)
    res = [0] * n
    reroot_dp(0, children, dp, res)
    print(*res)

if __name__ == "__main__":
    main()