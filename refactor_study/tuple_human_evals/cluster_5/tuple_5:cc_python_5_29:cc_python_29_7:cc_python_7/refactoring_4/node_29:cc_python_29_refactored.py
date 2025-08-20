from codebank import *
import sys

def main():
    s = sys.stdin.readline().strip()
    n = len(s)
    Z = z_function(s)
    # max_prefix[i] = max Z[1..i]
    max_prefix = [0]*n
    for i in range(1, n):
        max_prefix[i] = max(max_prefix[i-1], Z[i])
    # collect lengths of suffixes equal to a prefix
    lengths = [Z[i] for i in range(1, n) if i + Z[i] == n]
    lengths = sorted(set(lengths), reverse=True)
    for l in lengths:
        # check for an interior occurrence: any Z[j] >= l for j < n-l
        if n - l - 1 >= 1 and max_prefix[n - l - 1] >= l:
            print(s[:l])
            return
    print("Just a legend")

if __name__ == "__main__":
    main()