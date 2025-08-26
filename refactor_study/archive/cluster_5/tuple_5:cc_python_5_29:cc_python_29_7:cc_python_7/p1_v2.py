# ########## PROGRAM: node_29:cc_python_29 ##########

from codebank import *

def main():
    s = input().strip()
    n = len(s)
    Z = zfunction(s)
    borders = [Z[i] for i in range(1, n) if i + Z[i] == n]
    if not borders:
        print("Just a legend")
        return
    prefix_max = [0]*n
    for i in range(1, n):
        prefix_max[i] = max(prefix_max[i-1], Z[i])
    for L in sorted(borders, reverse=True):
        if prefix_max[n - L - 1] >= L:
            print(s[:L])
            return
    print("Just a legend")

if __name__ == "__main__":
    main()