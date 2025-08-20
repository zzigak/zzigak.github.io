from codebank import *

def main():
    n = int(input())
    arr = list(map(int, input().split()))
    p = int(input())
    dp = subsets_exact_counts(arr, p)
    ans = 0.0
    fact = n
    for i in range(1, n+1):
        ways = sum(dp[i][s] for s in range(p+1))
        ans += ways / fact
        fact *= (n - i)
    print(ans)

if __name__ == "__main__":
    main()