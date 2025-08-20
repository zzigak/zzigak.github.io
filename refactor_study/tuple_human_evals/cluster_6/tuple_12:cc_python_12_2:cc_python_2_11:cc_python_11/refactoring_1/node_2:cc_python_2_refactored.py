from codebank import *

def main():
    y, w = read_ints()
    num = 7 - max(y, w)
    num, den = reduce_frac(num, 6)
    print(f"{num}/{den}")

if __name__ == "__main__":
    main()