from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    MOD = 10**9 + 7
    n = int(input())
    count = {}
    for num in map(int, input().split()):
        for d in get_divisors(num):
            count[d] = count.get(d, 0) + 1
    maxk = max(count) if count else 0
    freq = {k: (pow_mod(2, c, MOD) - 1) % MOD for k, c in count.items()}
    for k in sorted(freq.keys(), reverse=True):
        for kk in range(k * 2, maxk + 1, k):
            if kk in freq:
                freq[k] = (freq[k] - freq[kk]) % MOD
    print(freq.get(1, 0))

if __name__ == "__main__":
    main()