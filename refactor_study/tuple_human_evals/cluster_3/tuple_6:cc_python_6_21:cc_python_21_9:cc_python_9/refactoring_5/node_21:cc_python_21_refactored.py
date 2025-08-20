from codebank import *

def main():
    n = int(input())
    beaver = list(map(int, input().split()))
    adj = read_tree(n)
    start = int(input()) - 1
    print(compute_max_beaver(n, beaver, adj, start))

if __name__ == "__main__":
    main()