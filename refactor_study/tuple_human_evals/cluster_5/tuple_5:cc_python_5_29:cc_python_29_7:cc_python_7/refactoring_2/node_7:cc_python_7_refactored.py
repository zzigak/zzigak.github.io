from codebank import *

MOD = 10**9 + 7

def compute_dp(s, bad_set):
    n = len(s)
    f = [0] * (n+1)
    f[n] = 1
    for j in range(n-1, -1, -1):
        for k in range(j+1, min(j+5, n+1)):
            if s[j:k] not in bad_set:
                f[j] = (f[j] + f[k]) % MOD
    return f

def main():
    import sys
    data = sys.stdin.read().split()
    m = int(data[0])
    bad_set = {"0011", "0101", "1110", "1111"}
    s = ""
    sm = 0
    idx = 1
    for _ in range(m):
        s += data[idx]
        idx += 1
        f = compute_dp(s, bad_set)
        z = zfunction(s[::-1])
        new = len(s) - max(z) if s else 0
        sm = (sm + sum(f[:new])) % MOD
        print(sm)

if __name__ == "__main__":
    main()