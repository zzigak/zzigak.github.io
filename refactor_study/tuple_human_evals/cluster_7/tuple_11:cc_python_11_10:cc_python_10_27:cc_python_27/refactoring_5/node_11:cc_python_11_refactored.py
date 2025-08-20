from codebank import *
import sys

MAX_BIT = 28

def main():
    input = sys.stdin.readline
    q = int(input())
    trie = trie_init(MAX_BIT)
    for _ in range(q):
        parts = list(map(int, input().split()))
        if parts[0] == 1:
            trie_insert(trie, parts[1], MAX_BIT)
        elif parts[0] == 2:
            trie_delete(trie, parts[1], MAX_BIT)
        else:
            print(trie_count_less_xor(trie, parts[1], parts[2], MAX_BIT))

if __name__ == "__main__":
    main()