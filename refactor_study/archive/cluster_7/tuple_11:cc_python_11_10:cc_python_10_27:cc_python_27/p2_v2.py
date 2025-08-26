# ########## PROGRAM: node_11:cc_python_11 ##########

from codebank import *

MAXB = 28

def main():
    import sys
    input = sys.stdin.readline
    q = int(input())
    root = {'cnt': 0}
    for _ in range(q):
        parts = list(map(int, input().split()))
        if parts[0] == 1:
            trie_insert(root, parts[1], 1, MAXB)
        elif parts[0] == 2:
            trie_insert(root, parts[1], -1, MAXB)
        else:
            pj, lj = parts[1], parts[2]
            print(trie_count_less(root, pj, lj, MAXB))

if __name__ == "__main__":
    main()