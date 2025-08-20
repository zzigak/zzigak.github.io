from codebank import *
import sys

MOD = 10**9 + 7
BAD = {(0,0,1,1),(0,1,0,1),(1,1,1,0),(1,1,1,1)}

def compute_dp(seq):
    n = len(seq)
    f = [0]*(n+1)
    f[n] = 1
    for j in range(n-1, -1, -1):
        tot = 0
        for k in range(j, min(j+4, n)):
            if tuple(seq[j:k+1]) not in BAD:
                tot = (tot + f[k+1]) % MOD
        f[j] = tot
    return f

def main():
    data = sys.stdin.read().split()
    m = int(data[0])
    bits = list(map(int, data[1:]))
    S = []
    sm = 0
    for b in bits:
        S.append(b)
        f = compute_dp(S)
        new = len(S) - max(zfunction(S[::-1]))
        sm = (sm + sum(f[:new])) % MOD
        print(sm)

if __name__ == "__main__":
    main()