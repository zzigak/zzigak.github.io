from codebank import *
import sys
def main():
    sys.setrecursionlimit(1000000)
    CONSTANT = 10**9 + 7
    data = sys.stdin.read().strip()
    if not data:
        return
    n = int(data)
    # Sieve for smallest prime factor (spf) and Omega (total prime multiplicity)
    spf = [0] * (n + 1)
    Omega = [0] * (n + 1)
    spf[1] = 1
    for i in range(2, n + 1):
        if spf[i] == 0:
            for j in range(i, n + 1, i):
                if spf[j] == 0:
                    spf[j] = i
        Omega[i] = Omega[i // spf[i]] + 1
    # Find maximum Omega and collect m with Omega[m] == k
    k = 0
    for i in range(2, n + 1):
        if Omega[i] > k:
            k = Omega[i]
    ms = [i for i in range(2, n + 1) if Omega[i] == k]
    # Precompute factorials up to n
    fact, invfact = precompute_factorials(n, CONSTANT)
    fact_n1 = fact[n - 1]
    # Memoization for F(d)
    memo = {1: 1}
    def F(d):
        if d == 1:
            return 1
        if d in memo:
            return memo[d]
        val_d = n // d
        denom = n - val_d
        invden = pow(denom, CONSTANT - 2, CONSTANT)
        res = 0
        # factor d via spf
        temp = d
        pf = []
        prev = 0
        cnt = 0
        while temp > 1:
            p = spf[temp]
            if p == prev:
                cnt += 1
            else:
                if prev != 0:
                    pf.append((prev, cnt))
                prev = p
                cnt = 1
            temp //= p
        if prev != 0:
            pf.append((prev, cnt))
        # sum over removing each prime
        for p, e in pf:
            d2 = d // p
            val_d2 = n // d2
            num = val_d2 - val_d
            factor = num * invden % CONSTANT
            res = (res + e * factor % CONSTANT * F(d2)) % CONSTANT
        memo[d] = res
        return res
    # Sum contributions
    ans = 0
    for m in ms:
        # divide by product of e_p! to account for identical primes
        inv_mult = 1
        temp = m
        while temp > 1:
            p = spf[temp]
            cnt = 0
            while temp % p == 0:
                temp //= p
                cnt += 1
            inv_mult = inv_mult * invfact[cnt] % CONSTANT
        hm = F(m) * inv_mult % CONSTANT
        ans = (ans + hm) % CONSTANT
    ans = ans * fact_n1 % CONSTANT
    print(ans)

if __name__ == "__main__":
    main()