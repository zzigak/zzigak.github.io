from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    n = int(input())
    beaver = list(map(int, input().split()))
    adj = read_tree(n)
    start = int(input()) - 1
    print(compute_muncher(adj, beaver, start))

if __name__ == "__main__":
    main()