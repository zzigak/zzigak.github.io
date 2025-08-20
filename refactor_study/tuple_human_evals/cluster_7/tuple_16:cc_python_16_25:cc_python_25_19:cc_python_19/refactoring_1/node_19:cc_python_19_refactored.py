from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    n = int(input())
    A = list(map(int, input().split()))
    P = list(map(int, input().split()))
    max_bit = max(max(A, default=0), max(P, default=0)).bit_length() - 1
    trie = [[0, 0, 0]]
    for x in P:
        trie_add(trie, x, max_bit)
    res = [trie_find_min_xor(trie, x, max_bit) for x in A]
    print(*res)

if __name__ == "__main__":
    main()