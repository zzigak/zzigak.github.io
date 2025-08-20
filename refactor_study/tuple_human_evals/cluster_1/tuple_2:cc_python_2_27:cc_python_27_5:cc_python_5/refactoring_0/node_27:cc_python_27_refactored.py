from codebank import *

MOD = 10**9 + 7

def main():
    import sys
    data = sys.stdin.read().split()
    n = int(data[0])
    arr = map(int, data[1:])
    count = {}
    for num in arr:
        for d in get_divisors(num):
            count[d] = count.get(d, 0) + 1
    maxk = max(count) if count else 0
    freq = {k: (pow_mod(2, count[k], MOD) - 1) % MOD for k in count}
    for k in sorted(count, reverse=True):
        for kk in range(k * 2, maxk + 1, k):
            if kk in freq:
                freq[k] = (freq[k] - freq[kk]) % MOD
    print(freq.get(1, 0))

if __name__ == "__main__":
    main()