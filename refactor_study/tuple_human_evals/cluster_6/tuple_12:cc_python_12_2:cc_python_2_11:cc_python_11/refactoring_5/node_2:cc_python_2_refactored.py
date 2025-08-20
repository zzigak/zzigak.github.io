from codebank import *

def main():
    x, y = read_ints()
    z = 7 - max(x, y)
    num, den = reduce_fraction(z, 6)
    print(f"{num}/{den}")

if __name__ == "__main__":
    main()