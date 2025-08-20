from codebank import *

def main():
    import sys
    stdin = sys.stdin
    n = int(stdin.readline())
    a = list(map(int, stdin.readline().split()))
    ops = solve_all(a)
    if ops is None:
        print("NO")
        return
    print("YES")
    print(len(ops))
    for x, y, z in ops:
        print(x, y, z)

if __name__ == "__main__":
    main()