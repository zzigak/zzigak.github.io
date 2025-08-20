from codebank import *
import sys
sys.setrecursionlimit(10**7)

def main():
    n = int(input())
    colors = list(read_ints())
    adj = read_tree(n)
    # white = 1, black = -1
    w = [1 if c == 1 else -1 for c in colors]
    par, order = parorder(adj, 0)
    dp1 = compute_dp1(adj, order, par, w)
    dp2 = compute_dp2(adj, order, par, dp1)
    print(' '.join(str(x) for x in dp2))

if __name__ == "__main__":
    main()