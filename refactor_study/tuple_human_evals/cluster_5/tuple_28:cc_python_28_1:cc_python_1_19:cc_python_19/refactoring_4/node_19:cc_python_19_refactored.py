from codebank import *

def main():
    mod = 10**9 + 7
    s = read_str()
    print(compute_ab_steps(s, mod))

if __name__ == "__main__":
    main()