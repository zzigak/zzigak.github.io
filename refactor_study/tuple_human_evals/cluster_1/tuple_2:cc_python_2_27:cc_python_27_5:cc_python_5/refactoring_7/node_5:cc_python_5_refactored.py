from codebank import *

def main():
    t = int(input())
    for _ in range(t):
        a, b = map(int, input().split())
        if a == b:
            print(0)
            continue
        x, y = min(a, b), max(a, b)
        if y % x != 0 or ((y // x) & (y // x) - 1) != 0:
            print(-1)
        else:
            print(min_operations_for_power_of_two_ratio(y // x))

if __name__ == "__main__":
    main()