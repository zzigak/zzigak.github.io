from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    n = int(input())
    vals = list(map(int, input().split()))
    xori = 0
    ans = 0
    mul = 1
    for _ in range(32):
        inv0, inv1 = bit_inversion_counts(vals)
        if inv0 <= inv1:
            ans += inv0
        else:
            ans += inv1
            xori += mul
        mul <<= 1
        vals = [v >> 1 for v in vals]
    print(ans, xori)

if __name__ == "__main__":
    main()