from codebank import *
import sys
sys.setrecursionlimit(10**7)

def main():
    n = int(input())
    w = list(map(int, input().split()))
    adj = read_weighted_tree(n)
    print(max_weighted_path(w, adj))

if __name__ == "__main__":
    main()