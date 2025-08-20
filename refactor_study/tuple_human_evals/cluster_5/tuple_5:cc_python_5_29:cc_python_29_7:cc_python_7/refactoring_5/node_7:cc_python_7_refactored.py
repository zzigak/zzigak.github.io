from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    MOD = 10**9+7
    BAD = {"0011","0101","1110","1111"}
    m = int(input())
    S = ""
    sm = 0
    for _ in range(m):
        S += input().strip()
        n = len(S)
        f = [0]*(n+1)
        f[n] = 1
        for j in range(n-1, -1, -1):
            for l in range(1, 5):
                if j + l <= n and S[j:j+l] not in BAD:
                    f[j] = (f[j] + f[j+l]) % MOD
        Z = z_function(S[::-1])
        new = n - max(Z)
        for x in f[:new]:
            sm = (sm + x) % MOD
        print(sm)

if __name__ == "__main__":
    main()