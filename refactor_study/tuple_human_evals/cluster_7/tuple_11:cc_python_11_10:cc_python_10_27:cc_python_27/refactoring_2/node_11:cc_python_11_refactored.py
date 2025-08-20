from codebank import trie_init, trie_add, trie_count_xor_less

BITS = 28

def main():
    import sys
    input = sys.stdin.readline
    q = int(input())
    trie = trie_init()
    for _ in range(q):
        evt = list(map(int, input().split()))
        t = evt[0]
        if t == 1:
            trie_add(trie, evt[1], 1, BITS)
        elif t == 2:
            trie_add(trie, evt[1], -1, BITS)
        else:
            p, l = evt[1], evt[2]
            print(trie_count_xor_less(trie, p, l, BITS))

if __name__ == "__main__":
    main()