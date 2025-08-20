from codebank import *

def main():
    w, b = read_ints()
    result = compute_dp_probability(w, b)
    print(f"{result:.9f}")

if __name__ == "__main__":
    main()