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
        if a > b:
            a, b = b, a
        if b % a != 0:
            print(-1)
            continue
        ratio = b // a
        if not is_power_of_two(ratio):
            print(-1)
        else:
            exp = ratio.bit_length() - 1
            print(count_power2_factors(exp))

if __name__ == "__main__":
    main()