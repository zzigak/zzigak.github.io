from codebank import *

def main():
    x, y = read_ints()
    z = 7 - max(x, y)
    n, d = reduce_fraction(z, 6)
    print(f"{n}/{d}")

if __name__ == "__main__":
    main()