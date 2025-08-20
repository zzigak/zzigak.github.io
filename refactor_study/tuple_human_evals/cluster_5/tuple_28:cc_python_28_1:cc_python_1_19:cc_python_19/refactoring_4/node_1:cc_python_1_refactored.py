from codebank import *

def main():
    n = read_int()
    c = cnt(read_str())
    for _ in range(n - 1):
        c = nxt(c, read_str())
    print(max(c.values()))

if __name__ == "__main__":
    main()