from codebank import *

CONSTANT = 28

def main():
    import sys
    input = sys.stdin.readline
    q = int(input())
    trie = [[0,0,0]]
    for _ in range(q):
        line = input().split()
        t = int(line[0])
        if t == 1:
            trie_update(trie, int(line[1]), 1, CONSTANT)
        elif t == 2:
            trie_update(trie, int(line[1]), -1, CONSTANT)
        else:
            pi = int(line[1]); li = int(line[2])
            print(trie_count_less(trie, pi, li, CONSTANT))

if __name__ == "__main__":
    main()