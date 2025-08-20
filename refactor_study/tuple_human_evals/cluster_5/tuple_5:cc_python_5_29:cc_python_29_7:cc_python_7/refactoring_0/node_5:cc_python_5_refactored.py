import sys
from codebank import *

def main():
    input = sys.stdin.readline
    n = int(input())
    a = read_ints()
    # compress values to 1..n
    vals = sorted(a)
    comp = {v:i+1 for i,v in enumerate(vals)}
    bit0 = [0] * (n + 1)
    bit1 = [0] * (n + 1)
    ans = 0
    for v in reversed(a):
        idx = comp[v]
        # count pairs i<j<k with a[i]>a[j]>a[k]
        ans += bit_query(bit1, idx-1)
        # update counts of suffix elements
        bit_update(bit0, n, idx, 1)
        # update counts of pairs ending at this v
        bit_update(bit1, n, idx, bit_query(bit0, idx-1))
    print(ans)

if __name__ == "__main__":
    main()