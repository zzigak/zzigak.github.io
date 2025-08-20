from codebank import *

def main():
    ALPH = 'abcdefghijklmnopqrstuvwxyz'
    MAX = 10**9
    n = read_int()
    c = cnt(read_str())
    for _ in range(n - 1):
        c = nxt(c, read_str(), ALPH, MAX)
    print(max(c.values()))

if __name__ == "__main__":
    main()