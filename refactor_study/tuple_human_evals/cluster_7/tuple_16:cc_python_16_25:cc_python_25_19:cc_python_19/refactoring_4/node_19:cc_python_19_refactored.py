from codebank import *

def main():
    import sys
    data = sys.stdin.read().split()
    it = iter(data)
    n = int(next(it))
    A = [int(next(it)) for _ in range(n)]
    P = [int(next(it)) for _ in range(n)]
    BIT_MAX = 30
    tree = build_trie(P, BIT_MAX)
    res = []
    for a in A:
        res.append(str(pop_min_xor(tree, a, BIT_MAX)))
    print(" ".join(res))

if __name__ == "__main__":
    main()