from codebank import *

def main():
    n = int(input()); a = list(map(int,input().split())); p = int(input())
    fact = factorials(n)
    ans = 0.0
    for idx, v in enumerate(a):
        arr = a[:idx] + a[idx+1:]
        dp = count_subsets_by_size(arr, p)
        threshold = p - v + 1
        for k in range(n):
            if threshold <= p:
                ways = sum(dp[k][threshold:])
                ans += k * ways * fact[k] * fact[n-k-1]
    print(ans / fact[n])

if __name__ == "__main__":
    main()