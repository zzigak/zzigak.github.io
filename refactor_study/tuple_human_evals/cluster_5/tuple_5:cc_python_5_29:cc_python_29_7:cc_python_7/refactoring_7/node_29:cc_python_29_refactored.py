from codebank import *

def main():
    import sys
    s = sys.stdin.readline().strip()
    Z = z_function(s)
    n = len(s)
    # build prefix maximum of Z
    pmx = [0]*n
    for i in range(1, n):
        pmx[i] = pmx[i-1] if pmx[i-1] > Z[i] else Z[i]
    # collect all border lengths
    borders = [Z[i] for i in range(1, n) if i + Z[i] == n]
    borders.sort(reverse=True)
    for L in borders:
        # check if border of length L appears strictly inside (not as suffix)
        if n - L - 1 >= 1 and pmx[n - L - 1] >= L:
            print(s[:L])
            break
    else:
        print("Just a legend")

if __name__ == "__main__":
    main()