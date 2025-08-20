from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    n = int(input())
    b = list(map(int, input().split()))
    a = list(map(int, input().split()))
    diff = [b[i] - a[i] for i in range(n)]
    par = [-1] * n
    factor = [1] * n
    for i in range(1, n):
        x, k = map(int, input().split())
        par[i] = x - 1
        factor[i] = k
    possible = can_conduct_experiment(diff, par, factor)
    print("YES" if possible else "NO")

if __name__ == "__main__":
    main()