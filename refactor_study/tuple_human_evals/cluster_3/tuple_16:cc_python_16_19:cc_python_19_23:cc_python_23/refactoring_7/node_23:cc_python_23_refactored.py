from codebank import *
import sys
input = sys.stdin.buffer.readline

def main():
    n, k = map(int, input().split())
    adj = read_tree(n)
    mod = 998244353
    ans = compute_valid_sets(adj, k, mod)
    print(ans)

if __name__ == "__main__":
    main()