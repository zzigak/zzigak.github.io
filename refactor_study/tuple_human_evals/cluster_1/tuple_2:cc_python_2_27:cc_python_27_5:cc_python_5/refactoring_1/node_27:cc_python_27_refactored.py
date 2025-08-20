from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    MOD = 10**9 + 7

    n = int(input())
    nums = list(map(int, input().split()))
    count = {}
    for num in nums:
        for d in get_divisors(num):
            count[d] = count.get(d, 0) + 1

    maxd = max(count)
    freq = {d: (pow_mod(2, c, MOD) - 1) % MOD for d, c in count.items()}
    # inclusion–exclusion: subtract multiples
    for d in sorted(freq.keys(), reverse=True):
        for m in range(d*2, maxd+1, d):
            if m in freq:
                freq[d] = (freq[d] - freq[m]) % MOD

    print(freq.get(1, 0))

if __name__ == "__main__":
    main()