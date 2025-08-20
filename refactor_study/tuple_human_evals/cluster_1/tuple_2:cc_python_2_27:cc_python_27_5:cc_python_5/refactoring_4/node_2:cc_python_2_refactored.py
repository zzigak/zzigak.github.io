from codebank import *

def main():
    a, b = map(int, input().split())
    if a == b:
        print(0)
        return
    primes = [2, 3, 5]
    a_exps, a_res = extract_exponents_and_residual(a, primes)
    b_exps, b_res = extract_exponents_and_residual(b, primes)
    if a_res != b_res:
        print(-1)
    else:
        ops = sum(abs(a_exps[p] - b_exps[p]) for p in primes)
        print(ops)

if __name__ == "__main__":
    main()