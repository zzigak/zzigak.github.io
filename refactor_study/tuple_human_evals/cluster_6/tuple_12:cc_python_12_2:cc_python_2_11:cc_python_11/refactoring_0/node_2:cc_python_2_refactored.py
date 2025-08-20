from codebank import *

def main():
    x, y = read_ints()
    num, den = process_die_probability(x, y)
    print_fraction(num, den)

if __name__ == "__main__":
    main()