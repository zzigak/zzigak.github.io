from codebank import *

def main():
    n = int(input())
    a = list(read_ints())
    weights = [1 if x else -1 for x in a]
    adj = read_tree(n)
    res = tree_reroot(adj, weights)
    print(*res)

if __name__ == "__main__":
    main()