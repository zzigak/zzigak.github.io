from codebank import *

def main():
    import sys
    u, v = map(int, sys.stdin.readline().split())
    res = solve_xor_sum(u, v)
    if res is None:
        print(-1)
    else:
        print(len(res))
        if res:
            print(*res)

if __name__ == "__main__":
    main()