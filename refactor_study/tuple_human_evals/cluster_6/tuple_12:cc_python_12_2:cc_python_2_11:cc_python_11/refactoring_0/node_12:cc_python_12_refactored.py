from codebank import *

def main():
    w, b = read_ints()
    print(f"{compute_princess_win_prob(w, b):.9f}")

if __name__ == "__main__":
    main()