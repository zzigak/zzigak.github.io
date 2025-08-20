from codebank import *

def main():
    w, b = read_ints()
    res = compute_princess_probability(w, b)
    print("{:.9f}".format(res))

if __name__ == "__main__":
    main()