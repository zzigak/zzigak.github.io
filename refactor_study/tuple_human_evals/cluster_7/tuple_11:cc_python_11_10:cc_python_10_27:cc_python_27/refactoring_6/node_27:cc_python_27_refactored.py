from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    n = int(input())
    a = list(map(int, input().split()))
    ops = []
    if n <= 10:
        sol = solve_small(a.copy())
        if sol is None:
            print("NO")
            return
        print("YES")
        print(len(sol))
        for x, y, z in sol:
            print(x, y, z)
        return
    solve_large(a, ops)
    while len(a) < 8:
        a.append(0)
    sol = solve_small(a)
    print("YES")
    ops += sol
    print(len(ops))
    for x, y, z in ops:
        print(x, y, z)

if __name__ == "__main__":
    main()