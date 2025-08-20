from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    n = int(input())
    arr = list(map(int, input().split()))
    ans = x = 0
    mul = 1
    for _ in range(32):
        inv1, inv2, arr = calc_bit_inversions_and_shift(arr)
        if inv1 <= inv2:
            ans += inv1
        else:
            ans += inv2
            x |= mul
        mul <<= 1
    print(ans, x)

if __name__ == "__main__":
    main()