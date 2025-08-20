from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    n = int(input())
    arr = list(map(int, input().split()))
    xori = 0
    ans = 0
    mul = 1
    for _ in range(32):
        inv1, inv2 = count_bit_inversions(arr)
        if inv1 <= inv2:
            ans += inv1
        else:
            ans += inv2
            xori += mul
        mul <<= 1
        arr = [v >> 1 for v in arr]
    print(ans, xori)

if __name__ == "__main__":
    main()