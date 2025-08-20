from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    n = int(input())
    arr = list(map(int, input().split()))
    ans = 0
    xori = 0
    # arr_current stores the remaining bits of each a_i,
    # shifting off one bit per iteration
    arr_current = arr[:]
    # a_i ≤ 10^9 < 2^30, so we process bits 0..30
    for bit in range(31):
        inv0, inv1 = compute_inv_for_bit(arr_current)
        if inv1 < inv0:
            ans += inv1
            xori |= (1 << bit)
            # flip the LSB then shift right
            arr_current = [(num ^ 1) >> 1 for num in arr_current]
        else:
            ans += inv0
            arr_current = [num >> 1 for num in arr_current]
    print(ans, xori)

if __name__ == "__main__":
    main()