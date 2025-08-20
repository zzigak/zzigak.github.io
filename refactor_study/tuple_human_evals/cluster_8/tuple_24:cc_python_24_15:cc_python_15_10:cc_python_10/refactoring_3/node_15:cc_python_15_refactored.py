from codebank import *

def main():
    import sys
    data = sys.stdin.read().split()
    n = int(data[0])
    p = 10**9 + 7
    a, b, d, k = compute_counts(n)
    fact, _ = precompute_factorials(n, p)
    y = fact[n]
    s = k if n < 3 * (2 ** (k - 1)) else 0
    t = 0
    for j in range(s, k + 1):
        e = a[:j] + [d[j]] + b[j:]
        x = y * prod_mod(e, p) % p
        fseq = [sum(e[:i + 1]) for i in range(k + 1)]
        f = prod_mod(fseq, p)
        while f > 1:
            mf = p // f + 1
            x = x * mf % p
            f = f * mf % p
        t = (t + x) % p
    print(t)

if __name__ == "__main__":
    main()