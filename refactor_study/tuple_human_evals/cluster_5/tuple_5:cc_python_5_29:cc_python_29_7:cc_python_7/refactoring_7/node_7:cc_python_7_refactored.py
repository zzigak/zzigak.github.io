from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    MOD = 10**9 + 7
    BAD = {"0011", "0101", "1110", "1111"}
    m = int(input())
    S = ''
    sm = 0
    for _ in range(m):
        S += input().strip()
        f = count_splits_suffix(S, BAD)
        Z = z_function(S[::-1])
        new = len(S) - max(Z) if Z else len(S)
        for j in range(new):
            sm = (sm + f[j]) % MOD
        print(sm)

if __name__ == "__main__":
    main()