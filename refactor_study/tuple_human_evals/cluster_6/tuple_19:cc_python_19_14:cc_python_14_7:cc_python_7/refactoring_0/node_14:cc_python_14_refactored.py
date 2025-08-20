from codebank import *

def main():
    n = int(input())
    a = list(map(int, input().split()))
    p = int(input())
    if sum(a) <= p:
        print(n)
        return
    counts = count_sequences(a, p)
    ans = 0.0
    for i in range(1, n+1):
        ans += counts[i] / falling_factorial(n, i)
    print(ans)

if __name__ == "__main__":
    main()