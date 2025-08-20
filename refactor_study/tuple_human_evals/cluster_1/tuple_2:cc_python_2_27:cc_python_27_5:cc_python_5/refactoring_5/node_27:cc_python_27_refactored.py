from codebank import *

def main():
    import sys
    data = sys.stdin.read().split()
    n = int(data[0])
    arr = list(map(int, data[1:]))
    count = {}
    for num in arr:
        for d in get_divisors(num):
            count[d] = count.get(d, 0) + 1
    maxk = max(count.keys())
    MOD = 10**9 + 7
    freq = {k: (pow_mod(2, c, MOD) - 1) % MOD for k, c in count.items()}
    for k in sorted(count.keys(), reverse=True):
        for kk in range(2*k, maxk+1, k):
            if kk in freq:
                freq[k] = (freq[k] - freq[kk]) % MOD
    print(freq.get(1, 0))

if __name__ == "__main__":
    main()