from codebank import *

def main():
    w, b = read_ints()
    prob = compute_princess_win_prob(w, b)
    print(f"{prob:.9f}")

if __name__ == "__main__":
    main()