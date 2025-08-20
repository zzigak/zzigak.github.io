from codebank import *

def main():
    import sys
    data = sys.stdin
    n = int(data.readline())
    A = list(map(int, data.readline().split()))
    P = list(map(int, data.readline().split()))
    BITLEN = 30
    trie = init_xor_trie()
    for p in P:
        trie_insert(trie, p, BITLEN)
    out = []
    for a in A:
        out.append(trie_pop_min_xor(trie, a, BITLEN))
    print(*out)

if __name__ == "__main__":
    main()