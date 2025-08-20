from codebank import *

def main():
    n = int(input())
    b = list(map(int, input().split()))
    a = list(map(int, input().split()))
    parents = [-1] * n
    ks = [1] * n
    for i in range(1, n):
        x, k = map(int, input().split())
        parents[i] = x - 1
        ks[i] = k
    diff = compute_surplus(b, a)
    root_surplus = propagate_diff(diff, parents, ks)
    print("YES" if root_surplus >= 0 else "NO")

if __name__ == "__main__":
    main()