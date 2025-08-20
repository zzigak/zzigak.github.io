from codebank import *

def main():
    import sys, math
    mod = 10**9 + 7
    n = int(sys.stdin.readline())
    a = []
    x = n
    while x > 0:
        a.append(x - x//2)
        x //= 2
    k = int(math.log2(n))
    b = [n//(3*2**i) - n//(6*2**i) for i in range(k+1)]
    d = [n//2**i - n//(3*2**i) for i in range(k+1)]
    y = product_mod(range(2, n+1), mod)
    s = k if n < 3*2**(k-1) else 0
    t = 0
    for j in range(s, k+1):
        e = a[:j] + [d[j]] + b[j:k]
        x_val = y * product_mod(e, mod) % mod
        f_val = product_mod((sum(e[:i+1]) for i in range(k+1)), mod)
        while f_val > 1:
            m = mod//f_val + 1
            x_val = x_val * m % mod
            f_val = f_val * m % mod
        t = (t + x_val) % mod
    print(t)

if __name__ == "__main__":
    main()