from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    n = int(input())
    vals = list(map(int, input().split()))
    x = 0
    ans = 0
    MAX_BIT = 31
    for i in range(MAX_BIT + 1):
        inv0, inv1 = compute_bit_inversions(vals)
        if inv0 <= inv1:
            ans += inv0
        else:
            ans += inv1
            x |= 1 << i
        vals = shift_list(vals)
    print(ans, x)

if __name__ == "__main__":
    main()