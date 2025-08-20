from codebank import *

def main():
    w, b = read_ints()
    prob = compute_princess_win(w, b)
    print_float(prob, 9)

if __name__ == "__main__":
    main()