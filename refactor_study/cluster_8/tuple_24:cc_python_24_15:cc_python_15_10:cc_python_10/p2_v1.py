# ########## PROGRAM: node_15:cc_python_15 ##########

from codebank import prod
import math

def main():
    mod = 10**9 + 7
    n = int(input())
    x = n
    a = []
    while x > 0:
        a.append(x - x // 2)
        x //= 2
    k = int(math.log2(n))
    b = [n // (3 * (1 << i)) - n // (6 * (1 << i)) for i in range(k + 1)]
    d = [n // (1 << i) - n // (3 * (1 << i)) for i in range(k + 1)]
    y = prod(range(2, n + 1), mod)
    t = 0
    s = k if n < 3 * (1 << (k - 1)) else 0
    for j in range(s, k + 1):
        e = [a[i] for i in range(j)] + [d[j]] + [b[i] for i in range(j, k)]
        x_val = y * prod(e, mod) % mod
        f_val = prod([sum(e[:i+1]) for i in range(k + 1)], mod)
        while f_val > 1:
            x_val *= mod // f_val + 1
            f_val = f_val * (mod // f_val + 1) % mod
        t = (t + x_val) % mod
    print(t)

if __name__ == "__main__":
    main()