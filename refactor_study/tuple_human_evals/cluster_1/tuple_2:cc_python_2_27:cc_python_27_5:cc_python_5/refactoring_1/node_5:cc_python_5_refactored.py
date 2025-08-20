from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    t = int(input())
    for _ in range(t):
        a, b = map(int, input().split())
        print(min_shift_operations(a, b))

if __name__ == "__main__":
    main()