from codebank import *

def main():
    import sys
    data = sys.stdin.read().split()
    n = int(data[0])
    a = list(map(int, data[1:1+n]))
    p = list(map(int, data[1+n:1+2*n]))
    tree = [[0, 0, 0]]
    for x in p:
        trie_add(tree, x)
    out = [str(trie_pop_min_xor(tree, x)) for x in a]
    print(" ".join(out))

if __name__ == "__main__":
    main()