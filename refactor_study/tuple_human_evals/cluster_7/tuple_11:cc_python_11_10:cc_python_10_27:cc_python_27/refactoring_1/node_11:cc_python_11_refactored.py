from codebank import *

MAX_BIT = 28

def main():
    import sys
    input = sys.stdin.readline
    q = int(input())
    trie = init_trie()
    for _ in range(q):
        parts = input().split()
        tp = int(parts[0])
        if tp == 1:
            p = int(parts[1])
            trie_insert(trie, p, MAX_BIT)
        elif tp == 2:
            p = int(parts[1])
            trie_delete(trie, p, MAX_BIT)
        else:
            p = int(parts[1]); l = int(parts[2])
            print(count_xor_less(trie, p, l, MAX_BIT))

if __name__ == "__main__":
    main()