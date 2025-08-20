from codebank import *

def main():
    import sys
    data = sys.stdin.readline
    n = int(data())
    A = list(map(int, data().split()))
    P = list(map(int, data().split()))
    trie = create_trie()
    for x in P:
        trie_insert(trie, x, bitlen=29)
    O = [trie_remove_min_xor(trie, a, bitlen=29) for a in A]
    print(*O)

if __name__ == "__main__":
    main()