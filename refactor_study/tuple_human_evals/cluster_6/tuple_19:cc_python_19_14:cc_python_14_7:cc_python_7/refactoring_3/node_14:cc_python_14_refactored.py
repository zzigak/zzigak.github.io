from codebank import *

def main():
    n = int(input())
    arr = list(map(int, input().split()))
    p = int(input())
    if sum(arr) <= p:
        print(n)
        return
    fact = factorials(n)
    ans_num = 0
    for i in range(n):
        dp = subset_size_sum_counts(arr, i, p)
        for k in range(n):
            for s in range(p + 1):
                if s + arr[i] > p:
                    ans_num += k * dp[k][s] * fact[k] * fact[n - k - 1]
    print(ans_num / fact[n])

if __name__ == "__main__":
    main()