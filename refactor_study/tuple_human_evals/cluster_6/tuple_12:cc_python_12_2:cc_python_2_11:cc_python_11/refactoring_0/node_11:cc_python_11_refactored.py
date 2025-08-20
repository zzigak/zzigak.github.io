from codebank import *

def main():
    k, n, m = read_ints()
    a = read_ints()
    ops = [tuple(read_ints()) for _ in range(n)]
    seq = best_upgrades(k, a, ops, m)
    print(len(seq))
    if seq:
        print(" ".join(map(str, seq)))

if __name__ == "__main__":
    main()