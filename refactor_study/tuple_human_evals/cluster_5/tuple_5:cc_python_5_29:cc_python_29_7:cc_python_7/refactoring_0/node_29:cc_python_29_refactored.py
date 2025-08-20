from codebank import *
import sys

def main():
    input = sys.stdin.readline
    s = input().strip()
    n = len(s)
    Z = z_function(s)
    # build prefix maximum of Z to allow O(1) checks of any match before a given index
    prefix_max = [0] * n
    if n > 0:
        prefix_max[0] = Z[0]
    for i in range(1, n):
        prefix_max[i] = max(prefix_max[i-1], Z[i])
    # collect all border lengths L where prefix of length L == suffix of length L
    borders = []
    for i in range(1, n):
        if i + Z[i] == n:
            borders.append(Z[i])
    # try borders in descending order
    borders.sort(reverse=True)
    for L in borders:
        # check if there's an occurrence of this prefix of length L strictly inside
        # i.e., at some position i with 1 <= i <= n-L-1
        if n - L - 1 >= 0 and prefix_max[n - L - 1] >= L:
            print(s[:L])
            return
    print("Just a legend")

if __name__ == "__main__":
    main()