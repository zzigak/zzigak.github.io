from codebank import *

def main():
    n = int(input())
    arr = list(map(int, input().split()))
    p = int(input())
    dp = count_sequences(arr, p)
    ans = 0.0
    fact = n
    for i in range(1, n+1):
        ans += dp[i][p] / fact
        fact *= (n - i)
    print("{:.10f}".format(ans))

if __name__ == "__main__":
    main()