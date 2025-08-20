from codebank import *

CONSTANT = 30

def main():
    import sys
    data = sys.stdin
    q = int(data.readline())
    trie = init_trie(CONSTANT)
    for _ in range(q):
        l = list(map(int, data.readline().split()))
        op = l[0]
        if op == 1:
            trie_modify(trie, l[1], CONSTANT, 1)
        elif op == 2:
            trie_modify(trie, l[1], CONSTANT, -1)
        else:
            print(count_xor_less(trie, l[1], l[2], CONSTANT))

if __name__ == "__main__":
    main()