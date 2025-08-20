from codebank import *

BIT = 28

def main():
    import sys
    input = sys.stdin.readline
    q = int(input())
    root = trie_new()
    for _ in range(q):
        ev = list(map(int, input().split()))
        tp = ev[0]
        if tp == 1:
            trie_insert(root, ev[1], BIT, 1)
        elif tp == 2:
            trie_insert(root, ev[1], BIT, -1)
        else:
            p, limit = ev[1], ev[2]
            res = trie_count_less(root, p, limit, BIT)
            print(res)

if __name__ == "__main__":
    main()