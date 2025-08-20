from codebank import *

def main():
    x, y = read_ints()
    mx = max(x, y)
    fav = 6 - mx + 1
    numer, denom = reduce_fraction(fav, 6)
    print(f"{numer}/{denom}")

if __name__ == "__main__":
    main()