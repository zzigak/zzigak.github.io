from codebank import *

def main():
    n = int(input())
    adj = read_tree(n)
    vals = list(read_ints())
    print(tree_dp_balance(adj, vals))

if __name__ == "__main__":
    main()