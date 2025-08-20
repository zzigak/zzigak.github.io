from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    n, k = map(int, input().split())
    adj = read_tree(n)
    mod = 998244353
    print(count_valid_subsets(adj, k, mod))

if __name__ == "__main__":
    main()