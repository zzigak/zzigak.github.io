from codebank import *

MOD = 10**9 + 7

def compute_counts(n):
    k = n.bit_length() - 1
    x = n
    a = []
    while x > 0:
        a.append(x - x // 2)
        x //= 2
    b = [n // (3 * (1 << i)) - n // (6 * (1 << i)) for i in range(k + 1)]
    d = [n // (1 << i)     - n // (3 * (1 << i)) for i in range(k + 1)]
    return a, b, d, k

def factorial(n, mod):
    res = 1
    for i in range(2, n + 1):
        res = res * i % mod
    return res

def compute_s(n, k):
    return k if n < 3 * (1 << (k - 1)) else 0

def build_e(j, a, b, d, k):
    return a[:j] + [d[j]] + b[j:k]

def prefix_sums(lst):
    ps = []
    acc = 0
    for v in lst:
        acc += v
        ps.append(acc)
    return ps

def adjust_x(x, f, mod):
    while f > 1:
        t = mod // f + 1
        x = x * t % mod
        f = f * t % mod
    return x

def main():
    n = int(input())
    a, b, d, k = compute_counts(n)
    y = factorial(n, MOD)
    s = compute_s(n, k)
    total = 0
    for j in range(s, k + 1):
        e = build_e(j, a, b, d, k)
        x = y * product(e, MOD) % MOD
        f = product(prefix_sums(e), MOD)
        x = adjust_x(x, f, MOD)
        total = (total + x) % MOD
    print(total)

if __name__ == "__main__":
    main()