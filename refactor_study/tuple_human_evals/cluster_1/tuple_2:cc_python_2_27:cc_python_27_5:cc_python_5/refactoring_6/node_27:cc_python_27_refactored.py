from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    MOD = 10**9 + 7
    n = int(input())
    cnt = {}
    for num in map(int, input().split()):
        for d in get_divisors(num):
            cnt[d] = cnt.get(d, 0) + 1
    maxd = max(cnt) if cnt else 0
    freq = {k: (pow_mod(2, cnt[k], MOD) - 1) % MOD for k in cnt}
    for k in sorted(cnt.keys(), reverse=True):
        for m in range(k*2, maxd+1, k):
            if m in freq:
                freq[k] = (freq[k] - freq[m]) % MOD
    print(freq.get(1, 0) % MOD)

if __name__ == "__main__":
    main()