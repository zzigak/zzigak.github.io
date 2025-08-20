from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    n = int(input())
    A = list(map(int, input().split()))
    P = list(map(int, input().split()))
    trie = create_trie()
    for x in P:
        trie_add(trie, x)
    O = [trie_pop_min_xor(trie, x) for x in A]
    print(*O)

if __name__ == "__main__":
    main()