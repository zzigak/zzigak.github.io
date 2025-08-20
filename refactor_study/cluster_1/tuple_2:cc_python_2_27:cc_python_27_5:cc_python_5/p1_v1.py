# ########## PROGRAM: node_27:cc_python_27 ##########

from codebank import *

MOD = 10**9 + 7

def main():
    n = int(input().strip())
    arr = map(int, input().split())
    count = {}
    for num in arr:
        for d in get_divisors(num):
            count[d] = count.get(d, 0) + 1
    maxk = max(count.keys())
    freq = {d: (pow_mod(2, c, MOD) - 1) % MOD for d, c in count.items()}
    for d in sorted(count.keys(), reverse=True):
        for m in range(d*2, maxk+1, d):
            if m in freq:
                freq[d] = (freq[d] - freq[m]) % MOD
    print(freq.get(1, 0))

if __name__ == "__main__":
    main()