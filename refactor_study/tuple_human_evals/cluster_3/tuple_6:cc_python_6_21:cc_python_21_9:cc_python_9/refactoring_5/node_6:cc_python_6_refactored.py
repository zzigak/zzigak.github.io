from codebank import *

def main():
    n = int(input())
    w = list(map(int, input().split()))
    adj = read_weighted_tree(n)
    print(compute_max_gas(w, adj))

if __name__ == "__main__":
    main()