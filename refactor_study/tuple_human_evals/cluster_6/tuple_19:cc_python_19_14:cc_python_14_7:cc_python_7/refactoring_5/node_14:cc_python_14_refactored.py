from codebank import *

def main():
    import sys
    data = sys.stdin.read().split()
    n = int(data[0])
    arr = list(map(int, data[1:1+n]))
    p = int(data[1+n])
    fact = factorial_list(n)
    total = fact[n]
    if sum(arr) <= p:
        print(n)
        return
    ans = 0.0
    for i in range(n):
        other = arr[:i] + arr[i+1:]
        dp = permutation_counts(other, p)
        ai = arr[i]
        for k in range(n):
            for s in range(p+1):
                if s + ai > p:
                    ans += k * dp[k][s] * fact[n - k - 1]
    print(ans / total)

if __name__ == "__main__":
    main()