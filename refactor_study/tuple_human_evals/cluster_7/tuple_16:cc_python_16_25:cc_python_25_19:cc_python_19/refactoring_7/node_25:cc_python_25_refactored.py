from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    u, v = map(int, input().split())
    if u > v or (v - u) & 1:
        print(-1)
        return
    if u == v:
        if u == 0:
            print(0)
        else:
            print(1)
            print(u)
        return
    k = (v - u) // 2
    if k & u == 0:
        print(2)
        print(u + k, k)
    else:
        print(3)
        print(u, k, k)

if __name__ == "__main__":
    main()