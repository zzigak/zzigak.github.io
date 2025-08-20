from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    n = int(input())
    b = list(map(int, input().split()))
    a = list(map(int, input().split()))
    par = [-1]*n
    k = [1]*n
    for i in range(1, n):
        x, ki = read_ints()
        par[i] = x - 1
        k[i] = ki
    diff = [b[i] - a[i] for i in range(n)]
    for i in range(n-1, 0, -1):
        p = par[i]
        if diff[i] >= 0:
            diff[p] += diff[i]
        else:
            diff[p] += diff[i] * k[i]
    print("YES" if diff[0] >= 0 else "NO")

if __name__ == "__main__":
    main()