from codebank import *

def main():
    n = int(input())
    adj = read_tree(n)
    vals = list(map(int, input().split()))
    par, order = parorder(adj)
    children = get_children(par)
    plus, minus = compute_balances(order, children, vals)
    print(plus[0] + minus[0])

if __name__ == "__main__":
    main()