from codebank import *

def main():
    import sys
    data = sys.stdin.read().split()
    n = int(data[0])
    arr = list(map(int, data[1:1+n]))
    p = int(data[1+n])
    dp = permutation_counts(arr, p)
    fact = factorial_list(n)
    total = fact[n]
    ans = sum(dp[i][p] * fact[n - i] for i in range(1, n + 1)) / total
    print(ans)

if __name__ == "__main__":
    main()