# ########## PROGRAM: node_3:cc_python_3 ##########

from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    mod = 10**9 + 7
    n = int(input().strip())
    a = list(map(int, input().split()))
    if n == 1:
        print(a[0] % mod)
        return
    if n & 1:
        a = alternating_reduction(a, mod)
        n -= 1
    fact, invfact = precompute_factorials(n, mod)
    sm1, sm2 = combine_sum(a, fact, invfact, mod)
    sign = final_sign(n)
    print((sm1 + sign * sm2) % mod)

if __name__ == "__main__":
    main()