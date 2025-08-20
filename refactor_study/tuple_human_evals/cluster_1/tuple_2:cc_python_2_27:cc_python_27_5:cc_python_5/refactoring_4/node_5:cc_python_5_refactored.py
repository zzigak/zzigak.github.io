from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    t = int(input())
    for _ in range(t):
        a, b = map(int, input().split())
        if a == b:
            print(0)
            continue
        if a < b:
            a, b = b, a
        if a % b != 0:
            print(-1)
            continue
        ratio = a // b
        ops = min_ops_for_ratio(ratio)
        print(ops if ops is not None else -1)

if __name__ == "__main__":
    main()