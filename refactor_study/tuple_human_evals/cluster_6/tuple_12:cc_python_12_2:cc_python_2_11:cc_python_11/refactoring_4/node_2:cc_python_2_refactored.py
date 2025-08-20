from codebank import *

def main():
    x, y = map(int, input().split())
    z = 7 - max(x, y)
    n, d = reduce_fraction(z, 6)
    print(f"{n}/{d}")

if __name__ == "__main__":
    main()