from codebank import *

def main():
    a, b = map(int, input().split())
    if a == b:
        print(0)
        return
    primes = [2, 3, 5]
    counts_a, res_a = extract_counts_residual(a, primes)
    counts_b, res_b = extract_counts_residual(b, primes)
    if res_a != res_b:
        print(-1)
    else:
        moves = sum(abs(ca - cb) for ca, cb in zip(counts_a, counts_b))
        print(moves)

if __name__ == "__main__":
    main()