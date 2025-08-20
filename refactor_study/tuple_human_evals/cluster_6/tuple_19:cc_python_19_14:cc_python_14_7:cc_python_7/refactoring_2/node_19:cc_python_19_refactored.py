from codebank import *

def main():
    import sys
    data = sys.stdin.read().split()
    n = int(data[0])
    arr = list(map(int, data[1:1+n]))
    p = int(data[1+n])
    dp = subsets_exact_counts(arr, p)
    ans = 0.0
    fact = n
    for i in range(1, n+1):
        ways = sum(dp[i][s] for s in range(p+1))
        ans += ways / fact
        fact *= (n - i)
    print("{:.10f}".format(ans))

if __name__ == "__main__":
    main()