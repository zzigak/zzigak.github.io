from codebank import *

def main():
    import sys
    data = sys.stdin.read().split()
    n = int(data[0])
    arr = list(map(int, data[1:1+n]))
    p = int(data[1+n])
    dp = count_sequences(arr, p)
    ans = 0.0
    fact = n
    for i in range(1, n+1):
        ans += dp[i][p] / fact
        fact *= (n - i)
    print("{:.10f}".format(ans))

if __name__ == "__main__":
    main()