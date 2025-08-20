from codebank import *

def main():
    x, y = read_ints()
    n, d = compute_die_probability(x, y)
    print(f"{n}/{d}")

if __name__ == "__main__":
    main()