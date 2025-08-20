from codebank import *

def main():
    n = read_int()
    alph = 'abcdefghijklmnopqrstuvwxyz'
    MAX = 10**9
    c = max_run_lengths(read_str())
    for _ in range(n - 1):
        t = read_str()
        c = merge_counts(c, t, alph, MAX)
    print(max(c.values()))

if __name__ == "__main__":
    main()