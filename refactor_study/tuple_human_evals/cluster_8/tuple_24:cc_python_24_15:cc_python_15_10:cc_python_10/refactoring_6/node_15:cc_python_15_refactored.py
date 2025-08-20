from codebank import product

def main():
    import sys, math
    input = sys.stdin.readline
    mod = 10**9 + 7
    n = int(input())
    a = []
    k = int(math.log2(n))
    x = n
    while x > 0:
        a.append(x - x//2)
        x //= 2
    b = [n//(3*2**i) - n//(6*2**i) for i in range(k+1)]
    d = [n//2**i - n//(3*2**i) for i in range(k+1)]
    y = product(range(2, n+1), mod)
    s = k if n < 3 * 2**(k-1) else 0
    total = 0
    for j in range(s, k+1):
        e = a[:j] + [d[j]] + b[j:k]
        x1 = y * product(e, mod) % mod
        f = product((sum(e[:i+1]) for i in range(k+1)), mod)
        while f > 1:
            mul = mod//f + 1
            x1 = x1 * mul % mod
            f = f * mul % mod
        total = (total + x1) % mod
    print(total)

if __name__ == "__main__":
    main()