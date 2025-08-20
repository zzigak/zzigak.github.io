from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    MOD = 10**9 + 7
    n = int(input())
    arr = list(map(int, input().split()))
    max_v = max(arr)
    freq = [0] * (max_v + 1)
    for x in arr:
        freq[x] += 1
    cnt = [0] * (max_v + 1)
    for d in range(1, max_v + 1):
        for m in range(d, max_v + 1, d):
            cnt[d] += freq[m]
    f = [0] * (max_v + 1)
    for d in range(max_v, 0, -1):
        f[d] = (pow_mod(2, cnt[d], MOD) - 1) % MOD
        for m in range(2 * d, max_v + 1, d):
            f[d] = (f[d] - f[m]) % MOD
    print(f[1])

if __name__ == "__main__":
    main()