from codebank import *

def main():
    s = read_str()
    MOD = 10**9 + 7
    print(compute_steps(s, MOD))

if __name__ == "__main__":
    main()