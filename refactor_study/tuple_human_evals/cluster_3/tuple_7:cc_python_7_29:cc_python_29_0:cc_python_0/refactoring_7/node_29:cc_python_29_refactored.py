from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    n = int(input())
    adj = read_tree(n)
    v = list(map(int, input().split()))
    ans = min_moves_to_zero(adj, v)
    print(ans)

if __name__ == "__main__":
    main()