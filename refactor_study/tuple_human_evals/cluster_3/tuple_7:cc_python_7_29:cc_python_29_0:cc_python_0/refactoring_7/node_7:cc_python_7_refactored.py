from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    n = int(input())
    a = list(map(int, input().split()))
    vals = [1 if x == 1 else -1 for x in a]
    adj = read_tree(n)
    res = reroot_max_subtree(adj, vals)
    print(*res)

if __name__ == "__main__":
    main()