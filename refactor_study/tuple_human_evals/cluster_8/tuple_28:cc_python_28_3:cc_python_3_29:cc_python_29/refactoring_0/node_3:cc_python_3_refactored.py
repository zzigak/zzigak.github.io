from codebank import *
import sys

CONSTANT = 10**9 + 7

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    a = list(map(int, data[1:]))
    if n == 1:
        print(a[0] % CONSTANT)
        return
    fact, invfact = precompute_factorials(n, CONSTANT)
    a, oper = reduce_until_even(a, CONSTANT)
    result = weighted_sum(a, oper, fact, invfact, CONSTANT)
    print(result)

if __name__ == "__main__":
    main()