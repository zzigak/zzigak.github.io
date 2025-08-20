from codebank import *

MAXB = 28

def main():
    import sys
    data = sys.stdin
    q = int(data.readline())
    root = {'cnt': 0}
    for _ in range(q):
        parts = data.readline().split()
        t = int(parts[0])
        if t == 1:
            trie_update(root, int(parts[1]), 1, MAXB)
        elif t == 2:
            trie_update(root, int(parts[1]), -1, MAXB)
        else:
            pi = int(parts[1]); li = int(parts[2])
            print(trie_count_less(root, pi, li, MAXB))

if __name__ == "__main__":
    main()