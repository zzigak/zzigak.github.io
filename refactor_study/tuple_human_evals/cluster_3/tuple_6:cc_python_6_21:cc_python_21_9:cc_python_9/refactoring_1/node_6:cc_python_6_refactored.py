from codebank import *

def main():
    import sys
    n = int(sys.stdin.readline())
    w = list(map(int, sys.stdin.readline().split()))
    adj, cost = read_tree(n)
    print(max_path_gain(w, adj, cost, 0))

if __name__ == "__main__":
    main()