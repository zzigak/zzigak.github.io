from codebank import *

PRIMES = [2, 3, 5]

def main():
    a, b = map(int, input().split())
    if a == b:
        print(0)
        return
    counts_a, res_a = extract_factors(a, PRIMES)
    counts_b, res_b = extract_factors(b, PRIMES)
    if res_a != res_b:
        print(-1)
    else:
        ops = sum(abs(counts_a[p] - counts_b[p]) for p in PRIMES)
        print(ops)

if __name__ == "__main__":
    main()