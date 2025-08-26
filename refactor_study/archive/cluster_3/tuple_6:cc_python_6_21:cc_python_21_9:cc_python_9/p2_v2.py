# ########## PROGRAM: node_6:cc_python_6 ##########

from codebank import *

def main():
    n = int(input())
    w, adj, cost = read_weighted_tree(n)
    print(leaf_dp_max_gas(w, adj, cost))

if __name__ == "__main__":
    main()