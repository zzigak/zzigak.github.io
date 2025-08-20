from codebank import *

def main():
    w, b = read_ints()
    res = compute_princess_win_probability(w, b)
    print(f"{res:.9f}")

if __name__ == "__main__":
    main()