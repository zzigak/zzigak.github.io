from codebank import *

def main():
    s = read_str()
    MOD = 10**9 + 7
    print(count_steps_ab_to_bba(s, MOD))

if __name__ == "__main__":
    main()