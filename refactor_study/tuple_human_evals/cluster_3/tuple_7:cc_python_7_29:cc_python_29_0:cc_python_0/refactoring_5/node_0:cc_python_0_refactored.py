from codebank import *

def main():
    n = int(input())
    supply = list(map(int, input().split()))
    need = list(map(int, input().split()))
    # net balance b[i] = supply[i] - need[i]
    b = [0] * (n + 1)
    for i in range(1, n + 1):
        b[i] = supply[i - 1] - need[i - 1]
    par = [0] * (n + 1)
    k = [1] * (n + 1)
    for i in range(2, n + 1):
        x, ki = read_ints()
        par[i] = x
        k[i] = ki
    threshold = -10**17
    # propagate deficits up the parent chain
    for i in range(n, 1, -1):
        if b[i] >= 0:
            b[par[i]] += b[i]
        else:
            b[par[i]] += b[i] * k[i]
            if b[par[i]] < threshold:
                print("NO")
                return
    print("YES" if b[1] >= 0 else "NO")

if __name__ == "__main__":
    main()