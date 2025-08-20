from codebank import *

def main():
    import sys
    data = sys.stdin.read().split()
    n = int(data[0])
    A = list(map(int, data[1:1+n]))
    P = list(map(int, data[1+n:1+2*n]))
    trie = build_xor_trie(P, bitlen=30)
    out = []
    for x in A:
        d = trie_pop_min_xor(trie, x, bitlen=30)
        out.append(str(d))
    print(" ".join(out))

if __name__ == "__main__":
    main()